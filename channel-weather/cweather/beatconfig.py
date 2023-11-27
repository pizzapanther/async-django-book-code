import datetime


BEAT_SCHEDULE = {
  'weather': [
    {
      'type': 'fetch.all',
      'message': {'testing': 'one'},
      'schedule': datetime.timedelta(minutes=3)
    }
  ]
}
