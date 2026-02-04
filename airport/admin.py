from django.contrib import admin
from .models import Airport, AirportRoute


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    list_filter = ['name']


@admin.register(AirportRoute)
class AirportRouteAdmin(admin.ModelAdmin):
    list_display = ['id', 'parent', 'child', 'position', 'duration']
    list_filter = ['position', 'parent']
    search_fields = ['parent__name', 'child__name']
    ordering = ['parent', 'position']
