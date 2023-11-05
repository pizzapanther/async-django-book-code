from django.contrib import admin

from djstorm.models import WeatherPoint


@admin.register(WeatherPoint)
class WPAdmin(admin.ModelAdmin):
  list_display = ['point', 'created']
  date_hierarchy = 'created'
