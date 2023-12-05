from django.conf import settings
from django.http import StreamingHttpResponse, HttpResponse

import aiofiles
import aiofiles.os

# function copied from: https://github.com/wearespindle/django-ranged-fileresponse/blob/master/ranged_fileresponse/__init__.py#L41C5-L90C1
def parse_range_header(header, resource_size):
  """
  Parses a range header into a list of two-tuples (start, stop) where
  `start` is the starting byte of the range (inclusive) and
  `stop` is the ending byte position of the range (exclusive).

  Args:
      header (str): The HTTP_RANGE request header.
      resource_size (int): The size of the file in bytes.

  Returns:
      None if the value of the header is not syntatically valid.
  """
  if not header or '=' not in header:
    return None

  ranges = []
  units, range_ = header.split('=', 1)
  units = units.strip().lower()

  if units != 'bytes':
    return None

  for val in range_.split(','):
    val = val.strip()
    if '-' not in val:
      return None

    if val.startswith('-'):
      # suffix-byte-range-spec: this form specifies the last N bytes
      # of an entity-body.
      start = resource_size + int(val)
      if start < 0:
          start = 0
      stop = resource_size
    else:
      # byte-range-spec: first-byte-pos "-" [last-byte-pos].
      start, stop = val.split('-', 1)
      start = int(start)
      # The +1 is here since we want the stopping point to be
      # exclusive, whereas in the HTTP spec, the last-byte-pos
      # is inclusive.
      stop = int(stop) + 1 if stop else resource_size
      if start >= stop:
        return None

    ranges.append((start, stop))

  return ranges


async def stream_file (file_path, brange=None):
  async with aiofiles.open(file_path, mode='rb') as fh:
    at = 0

    if brange:
      await fh.seek(brange[0])
      at = brange[0]

    while 1:
      chunk = 4096
      if brange:
        if (at + chunk) > brange[1]:
          chunk = brange[1] - at

      contents = await fh.read(chunk)
      at = at + chunk

      if not contents:
        break

      yield contents

      if brange and brange[1] == at:
        break


async def video_stream(request):
  file_path = settings.BASE_DIR / 'files' / 'bunny.m4v'
  stats = await aiofiles.os.stat(file_path)
  file_size = stats.st_size

  if request.method == 'HEAD':
    print('HEAD Request')
    return HttpResponse(headers={
        'Accept-Ranges': 'bytes',
        'Content-Length': str(file_size)
      })

  ranges = parse_range_header(request.META.get('HTTP_RANGE'), file_size)
  print("RANGES:", ranges)

  status_code = 200
  headers = {
    'Accept-Ranges': 'bytes',
    'Content-Length': str(file_size)
  }

  # Only handle syntactically valid headers, that are simple (no multipart byteranges).
  # copied from https://github.com/wearespindle/django-ranged-fileresponse/blob/master/ranged_fileresponse/__init__.py#L131-L145
  brange = None
  if ranges is not None and len(ranges) == 1:
    brange = ranges[0]
    start, stop = ranges[0]
    if start >= file_size:
      # Requested range not satisfiable.
      status_code = 416
      return

    if stop >= file_size:
      stop = file_size

    headers['Content-Range'] = 'bytes %d-%d/%d' % (start, stop - 1, file_size)
    headers['Content-Length'] = stop - start
    status_code = 206

  return StreamingHttpResponse(
    (stream_file(file_path, brange)),
    content_type="video/x-m4v",
    headers=headers,
    status=status_code,
  )
