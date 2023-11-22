from django.urls import path

import luna_ws

urlpatterns = [
  path('graphql', luna_ws.GraphQLSubscriptionHandler),
]
