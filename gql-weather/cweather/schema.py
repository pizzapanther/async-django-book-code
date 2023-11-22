import asyncio

import graphene
from graphql import GraphQLError

import djstorm.schema


class Query(djstorm.schema.Query, graphene.ObjectType):
  pass

class CountDownSubscription:
  count_seconds = graphene.Int(up_to=graphene.Int())

  async def subscribe_count_seconds(root, info, up_to):
    if up_to > 30:
      raise GraphQLError('Count too high, must be <= 30')

    for i in range(up_to):
      print('TestSubs: ', i)
      yield i
      await asyncio.sleep(1)


class Subscription(djstorm.schema.WeatherSubscription, CountDownSubscription, graphene.ObjectType):
  pass

schema = graphene.Schema(
  query=Query,
  subscription=Subscription,
  auto_camelcase=False,
)
