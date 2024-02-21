from typing import Type

from .base import BaseAdapter
from .csv import CSVAdapter
from .json import JSONAdapter

Adapters: dict[str, Type[BaseAdapter]] = {".csv": CSVAdapter, ".json": JSONAdapter}
