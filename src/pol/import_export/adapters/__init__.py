from typing import Type

from .base import Adapter
from .csv import CSVAdapter

Adapters: dict[str, Type[Adapter]] = {".csv": CSVAdapter}
