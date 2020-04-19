import codecs
import csv
import datetime

from building.models import Building
from meter.models import Meter, MeterReading


class UnrecognisedCSVException(Exception):
    pass


BULK_CREATE_SIZE = 100


def save_data(uploaded_file):
    csv_reader = csv.reader(
        codecs.iterdecode(uploaded_file, "utf-8-sig"), delimiter=","
    )
    header_line = cleanse_line(next(csv_reader))
    model = identify_filetype(header_line)

    items_to_bulk_save = []
    for line in csv_reader:
        cleansed_line = cleanse_line(line)
        if not cleansed_line:
            break
        obj = create_object_from_data(cleansed_line, header_line, model)
        items_to_bulk_save.append(obj)
        if (
            len(items_to_bulk_save) + 1 % BULK_CREATE_SIZE + 1 == 0
        ):  # adding 1 ensures we don't save on the first pass.
            print(f"Saving")
            model.objects.bulk_create(items_to_bulk_save)
            items_to_bulk_save = []
    if items_to_bulk_save:
        model.objects.bulk_create(items_to_bulk_save)

    print("all items saved!")


def cleanse_line(line):
    """
    Return the line of data, but with any empty values removed.
    """
    return [part for part in line if part]


def identify_filetype(header_line):
    """
    Looks at the headers to determine which model fits the data,
    and returns that model, as well as any transformation functions
    needed for the model to parse the data correctly.
    """
    if header_line == ["id", "name"]:
        return Building
    if header_line == ["consumption", "meter_id", "reading_date_time"]:
        return MeterReading
    if header_line == ["building_id", "id", "fuel", "unit"]:
        return Meter
    raise UnrecognisedCSVException(
        f"Could not recognise the csv file based on the headers! The headers were : {header_line}"
    )


def create_object_from_data(line, header_line, model):
    """
    Create a dictionary where each key is the header from the csv column, and the value
    is the corresponding column value for the current row. We also apply any necessary transformations
    to each piece of data, so that it can be saved in the model correctly.
    For example, we convert datetime strings to datetime objects.

    We then explode the dictionary to give key value pairs which can be used to instatiate
    an instance of the relevant model.
    """
    transformations = model.csv_transformations
    return model(
        **{
            header: transformations[header_index](line[header_index])
            for header_index, header in enumerate(header_line)
        }
    )
