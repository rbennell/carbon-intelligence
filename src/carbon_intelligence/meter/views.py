from django.shortcuts import render, get_object_or_404

from dateutil import parser

# Create your views here.
from .models import Meter, MeterReading


def show_meter(request, meter_id):
    meter = get_object_or_404(Meter.objects, id=meter_id)
    filters = get_filters(request)
    meter_readings = get_meter_readings(meter, filters)

    return render(
        request, "meter.html", {"meter": meter, "meter_readings": meter_readings}
    )


def get_filters(request):
    """
    Parse the url query for any filters that could
    be applied to the data
    """
    filters = {}
    dt_from = request.GET.get("from")
    if dt_from:
        filters["reading_date_time__gte"] = parser.parse(dt_from)

    dt_until = request.GET.get("until")
    if dt_until:
        filters["reading_date_time__lt"] = parser.parse(dt_until)
    return filters


def get_meter_readings(meter, filters):
    return [reading.graph_data for reading in meter.meterreading_set.filter(**filters)]
