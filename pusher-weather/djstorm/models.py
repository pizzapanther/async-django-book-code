from functools import cached_property

from django.db import models
from django.conf import settings


class WeatherPoint(models.Model):
  point = models.CharField(max_length=25, db_index=True)
  weather_data = models.JSONField()
  created = models.DateTimeField(auto_now_add=True, db_index=True)

  class Meta:
    ordering = ["-created"]

  def __str__(self):
    return self.point

  @cached_property
  def location(self):
    for l in settings.WEATHER_LOCATIONS:
      key = "{},{}".format(*l['location'])
      if key == self.point:
        return l['name']
