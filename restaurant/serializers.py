from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from restaurant.models import *


class RestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["id", "name"]


class RestaurantAllFieldsSerializer(ModelSerializer):
    """
    For creation/update endpoints
    """
    class Meta:
        model = Restaurant
        exclude = ["user"]


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class CategoryAllFieldsSerializer(ModelSerializer):
    """
    For creation/update endpoints
    """
    class Meta:
        model = Category
        exclude = ["user"]

    def validate(self, data):
        validated_data = super().validate(data)
        restaurant = validated_data.get("restaurant")
        restaurants = Restaurant.objects.filter(
            user=self.context.get("request").user
        )
        if restaurant not in restaurants:
            raise ValidationError(
                f"You do not have the access to this restaurant"
            )
        return validated_data


class IngredientSerializer(ModelSerializer):
    """
    For creation/update endpoints
    """
    class Meta:
        model = Ingredient
        exclude = ["user"]

    def validate(self, data):
        validated_data = super().validate(data)
        dish = validated_data.get("dish")
        dishes = Dish.objects.filter(
            user=self.context.get("request").user
        )
        if dish not in dishes:
            raise ValidationError(
                f"You do not have the access to this dish"
            )
        return validated_data


class DishSerializer(ModelSerializer):
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Dish
        fields = ["name", "image", "ingredients"]


class DishAllFieldsSerializer(ModelSerializer):
    """
    For creation/update endpoints
    """
    class Meta:
        model = Dish
        exclude = ["user"]

    def validate(self, data):
        validated_data = super().validate(data)
        category = validated_data.get("category")
        categories = Subcategory.objects.filter(
            user=self.context.get("request").user
        )
        if category not in categories:
            raise ValidationError(
                f"You do not have the access to this subcategory"
            )
        return validated_data


class SubcategorySerializer(ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ["name", "cover"]


class SubcategoryAllFieldsSerializer(ModelSerializer):
    """
    For creation/update endpoints
    """
    class Meta:
        model = Subcategory
        exclude = ["user"]

    def validate(self, data):
        validated_data = super().validate(data)
        parent = validated_data.get("parent")
        categories = Category.objects.filter(
            user=self.context.get("request").user
        )
        if parent not in categories:
            raise ValidationError(
                f"You do not have the access to this category"
            )
        return validated_data
