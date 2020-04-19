from django.contrib import admin

# Register your models here.
from .models import Building


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("id", "name")
