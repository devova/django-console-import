import sys
from decimal import Decimal
from itertools import batched
from typing import Iterator

from pydantic import BaseModel, ValidationError
from tablib import Dataset

from pol.import_export import BATCH_SIZE


class Record(BaseModel):
    name: str
    external_id: str
    category: str
    latitude: Decimal
    longitude: Decimal
    ratings: str


class BaseAdapter:
    record_model = Record

    def __init__(self, filename: str):
        self.filename = filename

    def _iter_items(self) -> Iterator[record_model]:
        raise NotImplementedError

    def _iter_raw_chunks(self, stop_on_error: bool) -> Iterator[tuple]:
        for item in self._iter_items():
            try:
                rec = self.record_model.model_validate(item).model_dump()
            except ValidationError as e:
                print(f"Item: {item}")
                print(e)
                if stop_on_error:
                    sys.exit(1)  # FIXME: this is a crap bag
            else:
                yield tuple(rec[field] for field in Record.model_fields.keys())

    def iter_chunks(self, stop_on_error: bool) -> Iterator[Dataset]:
        for raw_chunks in batched(self._iter_raw_chunks(stop_on_error), BATCH_SIZE):
            yield Dataset(
                *raw_chunks,
                headers=list(Record.model_fields.keys()),
            )
