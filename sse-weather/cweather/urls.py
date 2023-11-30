"""
URL configuration for cweather project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path

import djstorm.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("weather/", djstorm.views.locations),
    re_path(r"weather/(-?\d{1,3}.\d{2}),(-?\d{1,3}.\d{2})/", djstorm.views.WeatherStream.as_view()),
]
