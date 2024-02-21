from decimal import Decimal
from itertools import batched
from typing import Iterator

from pydantic import BaseModel
from tablib import Dataset

from pol.import_export import BATCH_SIZE


class Record(BaseModel):
    name: str
    external_id: str
    category: str
    latitude: Decimal
    longitude: Decimal
    ratings: str


class Adapter:
    def __init__(self, filename: str):
        self.filename = filename

    def _iter_raw_chunks(self, stop_on_error: bool) -> Iterator[tuple]:
        raise NotImplementedError

    def iter_chunks(self, stop_on_error: bool) -> Iterator[Dataset]:
        for raw_chunks in batched(self._iter_raw_chunks(stop_on_error), BATCH_SIZE):
            yield Dataset(
                *raw_chunks,
                headers=list(Record.model_fields.keys()),
            )
