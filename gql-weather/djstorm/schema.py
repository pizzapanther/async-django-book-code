import asyncio

import graphene
from graphene import relay
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from djstorm.models import WeatherPoint


class WeatherPointNode(DjangoObjectType):
  class Meta:
    model = WeatherPoint
    filter_fields = {
      'point': ['exact'],
      'created': ['gt', 'gte', 'lt', 'lte'],
    }
    interfaces = (relay.Node, )


class WeatherSubscription:
  track_location = GenericScalar(location=graphene.String())

  async def subscribe_track_location(root, info, location):
    while 1:
      wp = await WeatherPoint.objects.filter(point=location).afirst()
      if wp:
        print("SENDING", wp.weather_data['current'])
        yield wp.weather_data['current']

      await asyncio.sleep(30)


class Query:
  weather_points = DjangoFilterConnectionField(WeatherPointNode)
