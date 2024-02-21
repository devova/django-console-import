import csv
import sys
from decimal import Decimal
from typing import Annotated, Iterator

from pydantic import Field, BeforeValidator, ValidationError

from . import Adapter
from .base import Record


def parse_ratings(v) -> str:
    # Remove curly braces and split the string by comma
    numbers_str = v.strip("{}").split(",")
    # Convert each number from string to float and then to integer
    numbers_int = [str(int(float(num))) for num in numbers_str]
    return ",".join(numbers_int)


class CSVRecord(Record):
    name: Annotated[str, Field(..., alias="poi_name")]
    external_id: Annotated[str, Field(..., alias="poi_id")]
    category: Annotated[str, Field(..., alias="poi_category")]
    latitude: Annotated[Decimal, Field(alias="poi_latitude")]
    longitude: Annotated[Decimal, Field(alias="poi_longitude")]
    ratings: Annotated[str, Field(alias="poi_ratings"), BeforeValidator(parse_ratings)]


class CSVAdapter(Adapter):
    def _iter_raw_chunks(self, stop_on_error: bool) -> Iterator[tuple]:
        with open(self.filename, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    rec = CSVRecord.model_validate(row).model_dump()
                except ValidationError as e:
                    print(f"Row: {row}")
                    print(e)
                    if stop_on_error:
                        sys.exit(1)  # FIXME: this is a crap bag
                else:
                    yield tuple(rec[field] for field in Record.model_fields.keys())
