from functools import lru_cache

from import_export import resources, fields
from import_export.resources import ResourceOptions
from import_export.widgets import ForeignKeyWidget, SimpleArrayWidget

from . import BATCH_SIZE
from ..models import Pol, Category


class IntSimpleArrayWidget(SimpleArrayWidget):
    def clean(self, value, row=None, **kwargs):
        return [int(el) for el in super().clean(value, row, **kwargs)]


class PolResourceMeta(ResourceOptions):
    model = Pol
    skip_unchanged = True
    import_id_fields = ("external_id", "category")
    fields = (
        "name",
        "external_id",
        "category",
        "latitude",
        "longitude",
        "ratings",
    )


class PolResource(resources.ModelResource):
    category = fields.Field(
        column_name="category",
        attribute="category",
        widget=ForeignKeyWidget(Category, field="name"),
    )
    ratings = fields.Field(
        column_name="ratings", attribute="ratings", widget=IntSimpleArrayWidget()
    )

    class Meta(PolResourceMeta):
        pass

    def before_import_row(self, row, **kwargs):
        ensure_category(row["category"])


class BulkPolResource(PolResource):
    class Meta(PolResourceMeta):
        use_bulk = True
        batch_size = BATCH_SIZE


@lru_cache(maxsize=BATCH_SIZE)
def ensure_category(name: str):
    Category.objects.get_or_create(name=name, defaults={"name": name})
