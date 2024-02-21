import csv
from decimal import Decimal
from typing import Annotated, Iterator

from pydantic import Field, BeforeValidator

from .base import BaseAdapter, Record


def parse_ratings(v) -> str:
    # Remove curly braces and split the string by comma
    numbers_str = v.strip("{}").split(",")
    # Convert each number from string to float and then to integer
    numbers_int = [str(int(float(num))) for num in numbers_str]
    return ",".join(numbers_int)


class CSVRecord(Record):
    name: Annotated[str, Field(alias="poi_name")]
    external_id: Annotated[str, Field(alias="poi_id")]
    category: Annotated[str, Field(alias="poi_category")]
    latitude: Annotated[Decimal, Field(alias="poi_latitude")]
    longitude: Annotated[Decimal, Field(alias="poi_longitude")]
    ratings: Annotated[str, Field(alias="poi_ratings"), BeforeValidator(parse_ratings)]


class CSVAdapter(BaseAdapter):
    record_model = CSVRecord

    def _iter_items(self) -> Iterator[record_model]:
        with open(self.filename, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield row
