import json
from decimal import Decimal
from typing import Iterator, Annotated

from pydantic import BeforeValidator, Field

from .base import BaseAdapter, Record


def merge_ratings(v: list[int]) -> str:
    return ",".join(map(str, v))


class JSONRecord(Record):
    name: str
    external_id: Annotated[str, Field(alias="id")]
    category: str
    latitude: Annotated[Decimal, Field(alias=["coordinates", "latitude"])]
    longitude: Annotated[Decimal, Field(alias=["coordinates", "longitude"])]
    ratings: Annotated[str, BeforeValidator(merge_ratings)]


class JSONAdapter(BaseAdapter):
    record_model = JSONRecord

    def _iter_items(self) -> Iterator[record_model]:
        with open(self.filename, "r") as jsonfile:
            records = json.load(jsonfile)
            for record in records:
                yield record
