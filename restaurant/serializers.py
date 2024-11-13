from rest_framework.serializers import ModelSerializer
from restaurant.models import *


class RestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["id", "name"]


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class DishSerializer(ModelSerializer):
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Dish
        fields = ["name", "image", "ingredients"]


class SubcategorySerializer(ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ["name", "cover"]


class MenuSerializer(ModelSerializer):
    class Meta:
        model = Menu
        fields = "__all__"
