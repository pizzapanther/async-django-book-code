from graphene import relay
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


class Query:
  weather_points = DjangoFilterConnectionField(WeatherPointNode)
