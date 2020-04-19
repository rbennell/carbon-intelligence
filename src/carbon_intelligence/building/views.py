from dateutil import parser
from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch

from .models import Building
from meter.models import Meter, MeterReading


def show_buildings(request):
    buildings = Building.objects.prefetch_related(
        Prefetch("meter_set", Meter.objects.all().order_by("fuel"))
    )
    return render(request, "buildings.html", {"buildings": buildings})


def show_building(request, building_id):
    meter_filters = get_meter_filters(request)
    reading_filters = get_reading_filters(request)

    building = get_object_or_404(Building.objects, id=building_id)
    meters = Meter.objects.filter(
        building_id=building_id, **meter_filters
    ).prefetch_related(
        Prefetch("meterreading_set", MeterReading.objects.filter(**reading_filters))
    )

    meter_data = {
        "Electricity": {},
        "Natural Gas": {},
        "Water": {},
    }

    for meter in meters:
        # TODO: handle missing data. append datetimes with no readings,
        # and plot red lines where gaps exist in the data between points.
        # if data_type == 'totals':

        meter_data[meter.fuel][meter.id] = [
            reading.graph_data for reading in meter.meterreading_set.all()
        ]

    return render(
        request,
        "building.html",
        {"building": building, "meters": meters, "meter_readings": meter_data},
    )


def get_meter_filters(request):
    filters = {}
    meter_ids = request.GET.get("meter_ids")
    if meter_ids:
        filters["id__in"] = meter_ids.split(",")

    fuels = request.GET.get("fuels")
    if fuels:
        filters["fuel__in"] = fuels.split(",")
    return filters


def get_reading_filters(request):
    """
    Parse the url query for any filters that could
    be applied to the data
    """
    filters = {}
    from_date = request.GET.get("from_date")
    if from_date:
        filters["reading_date_time__gte"] = parser.parse(from_date)

    until_date = request.GET.get("until_date")
    if until_date:
        filters["reading_date_time__lt"] = parser.parse(until_date)

    return filters
