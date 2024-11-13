import django_filters
from restaurant.models import Category, Subcategory, Dish


class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Subcategory
        fields = {
            'parent': ['exact'],
            'dishes__name': ['icontains']
        }


class DishFilter(django_filters.FilterSet):
    class Meta:
        model = Dish
        fields = {
            'name': ['icontains']
        }
