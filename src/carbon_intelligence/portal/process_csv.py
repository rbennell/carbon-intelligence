import codecs
import csv

from building.models import Building
from meter.models import Meter, MeterReading


class UnrecognisedCSVException(Exception):
    pass


def save_data(uploaded_file):
    csv_reader = csv.reader(codecs.iterdecode(uploaded_file, "utf-8"), delimiter=",")
    header_line = [header for header in next(csv_reader) if header]
    model = identify_filetype(header_line)
    for line in csv_reader:
        cleansed_line = [part for part in line if part]
        if not cleansed_line:
            continue
        obj = model(
            **{
                header: cleansed_line[header_index]
                for header_index, header in enumerate(header_line)
            }
        )


def identify_filetype(header_line):
    """
    Looks at the headers to determine which model fits the data,
    and returns that model.
    """
    if header_line == ["id", "name"]:
        return Building
