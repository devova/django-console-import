from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_cte import CTEManager


class Category(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name


class Pol(models.Model):
    objects = CTEManager()

    name = models.CharField(max_length=256)
    external_id = models.CharField(max_length=256, db_index=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="pols", null=True
    )
    # keep precision 1m, https://en.wikipedia.org/wiki/Decimal_degrees#Precision
    latitude = models.DecimalField(max_digits=8, decimal_places=5)
    longitude = models.DecimalField(max_digits=9, decimal_places=5)
    ratings = ArrayField(
        models.PositiveSmallIntegerField(
            validators=[MaxValueValidator(5), MinValueValidator(1)]
        )
    )
    description = models.TextField(blank=True, null=True)
