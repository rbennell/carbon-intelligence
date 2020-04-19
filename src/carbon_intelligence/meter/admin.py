from django.contrib import admin

# Register your models here.
from .models import Meter, MeterReading


@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    list_display = ["id", "building_id", "fuel", "unit"]
    list_filter = ["fuel"]


@admin.register(MeterReading)
class MeterReading(admin.ModelAdmin):
    list_display = ["id", "meter_id", "consumption", "reading_date_time"]
    list_filter = ["meter_id"]
