from decimal import Decimal
from typing import Annotated, Iterator

from pydantic import BeforeValidator
from pydantic_xml import BaseXmlModel, element

from .base import BaseAdapter, quantize


class DataRecord(BaseXmlModel):
    external_id: Annotated[str, element(tag="pid")]
    name: Annotated[str, element(tag="pname")]
    category: Annotated[str, element(tag="pcategory")]
    latitude: Annotated[Decimal, element(tag="platitude"), BeforeValidator(quantize)]
    longitude: Annotated[Decimal, element(tag="plongitude"), BeforeValidator(quantize)]
    ratings: Annotated[str, element(tag="pratings")]


class Records(BaseXmlModel, tag="RECORDS"):
    data_records: Annotated[list[DataRecord], element(tag="DATA_RECORD")]


class XMLAdapter(BaseAdapter):
    record_model = DataRecord

    def _iter_items(self) -> Iterator[DataRecord]:
        with open(self.filename, "r") as xmlfile:
            t = xmlfile.read()
            records = Records.from_xml(t)
            for record in records.data_records:
                yield record
