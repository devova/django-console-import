from django.contrib import admin
from django.db.models import Avg, Func, F
from django_cte import With

from .models import Pol


class PolAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "external_id", "category", "avg_rating")
    list_filter = ("category",)
    search_fields = ("id", "external_id")

    def get_queryset(self, request):
        # With raw query it could be implemented without Common Table Expression, the query would look like:
        # SELECT pol_pol.*, avg(unnested_ratings) as avg_rating FROM pol_pol, unnest(ratings) as unnested_ratings GROUP BY 1
        # but unfortunately, it is impossible to write such a query using Django ORM
        cte = With(
            Pol.objects.values("id").annotate(
                unnest_ratings=Func(F("ratings"), function="unnest")
            )
        )
        return (
            cte.join(super().get_queryset(request), id=cte.col.id)
            .with_cte(cte)
            .annotate(avg_rating=Avg(cte.col.unnest_ratings))
        )

    @staticmethod
    def avg_rating(obj):
        return obj.avg_rating


admin.site.register(Pol, PolAdmin)
