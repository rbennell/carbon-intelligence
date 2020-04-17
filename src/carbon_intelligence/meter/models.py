from django.db import models

# Create your models here.

METER_TYPE_CHOICES = [
    ("electricity", "Electricity"),
    ("gas", "Natural Gas"),
    ("water", "Water"),
]

UNIT_CHOICES = [
    ("kWh", "kWh"),
    ("m3", "m3"),
]


class Meter(models.Model):
    id = models.IntegerField(primary_key=True)
    building = models.ForeignKey(to="building.Building", on_delete=models.CASCADE)
    fuel = models.CharField(max_length=63, choices=METER_TYPE_CHOICES)
    unit = models.CharField(max_length=63, choices=UNIT_CHOICES)


class MeterReading(models.Model):
    meter = models.ForeignKey(to="meter.Meter", on_delete=models.CASCADE)
    consumption = models.FloatField()
    reading_date_time = models.DateTimeField()
