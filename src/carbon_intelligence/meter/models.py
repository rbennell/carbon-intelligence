import datetime

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

    # these are the transformations that would need to be applied to each column of data, in order, from the csv file.
    csv_transformations = [int, int, str, str]


def parse_meter_reading_datetime(dt):
    return datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M")


class MeterReading(models.Model):
    meter = models.ForeignKey(to="meter.Meter", on_delete=models.CASCADE)
    consumption = models.FloatField()
    reading_date_time = models.DateTimeField()

    # these are the transformations that would need to be applied to each column of data, in order, from the csv file.
    csv_transformations = [float, int, parse_meter_reading_datetime]

    class Meta:
        get_latest_by = ["reading_date_time"]

    @property
    def graph_data(self):
        return {"datetime": self.reading_date_time, "consumption": self.consumption}
