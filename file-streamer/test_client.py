#!/usr/bin/env python3

import httpx


def run_tests (video_url="http://localhost:8000/video", content_length=121283919):
  resp = httpx.get(video_url)
  print('Full Length Test:', len(resp.content), content_length)
  assert resp.headers['Content-Length'] == str(content_length)
  assert len(resp.content) == content_length
  assert resp.status_code == 200

  resp = httpx.get(video_url, headers={'Range': 'bytes=0-5000'})
  print('Chunk Test:', len(resp.content), 5001)
  assert len(resp.content) == 5001
  assert resp.status_code == 206

  resp = httpx.get(video_url, headers={'Range': 'bytes=0-1023'})
  print('Small Chunk Test:', len(resp.content), 1024)
  assert len(resp.content) == 1024
  assert resp.status_code == 206

  resp = httpx.get(video_url, headers={'Range': 'bytes=1024-2047'})
  print('Jump Chunk Test:', len(resp.content), 1024)
  assert len(resp.content) == 1024
  assert resp.status_code == 206

  end = content_length - 1024
  resp = httpx.get(video_url, headers={'Range': f'bytes=1024-{end}'})
  print('Large Jump Chunk Test:', len(resp.content), end - 1023)
  assert len(resp.content) == (end - 1023)
  assert resp.status_code == 206

if __name__ == "__main__":
  run_tests()
