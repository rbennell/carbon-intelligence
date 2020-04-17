from django.contrib import admin

# Register your models here.
from .models import Meter, MeterReading


@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    pass


@admin.register(MeterReading)
class MeterReading(admin.ModelAdmin):
    pass
