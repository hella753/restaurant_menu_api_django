from django_filters.rest_framework import DjangoFilterBackend
from restaurant.utils import DishFilter, CategoryFilter


class CustomFilterBackend(DjangoFilterBackend):
    def get_filterset_class(self, view, queryset=None):
        if view.action == "retrieve":
            return DishFilter
        else:
            return CategoryFilter
