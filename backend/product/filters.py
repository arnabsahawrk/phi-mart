from django_filters.rest_framework import FilterSet
from product import models


class ProductFilter(FilterSet):
    class Meta:
        model = models.Product
        fields = {
            "category_id": {"exact"},
            "price": {"gt", "lt"},
        }
