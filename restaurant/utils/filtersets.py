import django_filters
from restaurant.models import Category, Subcategory, Dish


class CategoryFilter(django_filters.FilterSet):
    """
    Filterset which filters the category by
    the parent category and dish name
    """
    class Meta:
        model = Subcategory
        fields = {
            'parent': ['exact'],
            'dishes__name': ['icontains']
        }


class DishFilter(django_filters.FilterSet):
    """
    Filterset which filters the dish by
    the dish name
    """
    class Meta:
        model = Dish
        fields = {
            'name': ['icontains']
        }
