from django_filters.rest_framework import DjangoFilterBackend
from restaurant.utils import DishFilter, CategoryFilter


class CustomFilterBackend(DjangoFilterBackend):
    """
    Custom filter backend switches between the dish
    and category filtersets depending on the action name.
    """
    def get_filterset_class(self, view, queryset=None):
        if view.action == "retrieve":
            return DishFilter
        else:
            return CategoryFilter
