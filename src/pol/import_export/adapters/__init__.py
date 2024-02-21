from typing import Type

from .base import BaseAdapter
from .csv import CSVAdapter
from .json import JSONAdapter
from .xml import XMLAdapter

Adapters: dict[str, Type[BaseAdapter]] = {
    ".csv": CSVAdapter,
    ".json": JSONAdapter,
    ".xml": XMLAdapter,
}
