from django.db import transaction
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
        fields = "__all__"

    def validate(self, data):
        validated_data = super().validate(data)
        restaurant = validated_data.get("restaurant")
        user = self.context.get("request").user
        restaurants = Restaurant.objects.filter(
            user=user
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
        fields = "__all__"


class DishSerializer(ModelSerializer):
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Dish
        fields = ["name", "image", "ingredients"]


class DishAllFieldsSerializer(ModelSerializer):
    """
    For creation/update endpoints
    """
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Dish
        fields = "__all__"

    def create(self, validated_data):
        if validated_data.get("ingredients") is None:
            dish = Dish.objects.create(**validated_data)
        else:
            ingredients = validated_data.pop("ingredients")
            with transaction.atomic():
                dish = Dish.objects.create(**validated_data)
                ingredient_names = [
                    ingredient["name"] for ingredient in ingredients
                ]
                filtered_ingredients = Ingredient.objects.filter(
                    name__in=ingredient_names
                )
                for ingredient in filtered_ingredients:
                    ingredient_names.remove(ingredient.name)
                ingredient_list = [
                    Ingredient(
                        name=ingredient
                    ) for ingredient in ingredient_names
                ]
                Ingredient.objects.bulk_create(ingredient_list)
                ingredient_list.extend(list(filtered_ingredients))
                dish.ingredients.set(ingredient_list)
        return dish

    def update(self, instance, validated_data):
        ingredients = validated_data.pop("ingredients")
        existing_ingredients = instance.ingredients.all()
        ingredient_names = [ingredient["name"] for ingredient in ingredients]
        qs = existing_ingredients.exclude(name__in=ingredient_names)
        for ing in qs:
            if len(Dish.objects.filter(ingredients=ing)) == 1:
                ing.delete()
        existing_ingredients = Ingredient.objects.filter(
            name__in=ingredient_names
        )
        existing_ingredient_names = [
            ingredient.name for ingredient in existing_ingredients
        ]
        ingredients_to_create = [
            ingredient for ingredient in ingredient_names
            if ingredient not in existing_ingredient_names
        ]
        ingredient_list = [
            Ingredient(
                name=ingredient
            ) for ingredient in ingredients_to_create
        ]
        Ingredient.objects.bulk_create(ingredient_list)
        ingredient_list.extend(list(existing_ingredients))
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.ingredients.set(ingredient_list)
        return instance

    def validate(self, data):
        validated_data = super().validate(data)
        category = validated_data.get("category")
        user = self.context.get("request").user

        categories = Subcategory.objects.filter(
            parent__restaurant__user=user
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
        fields = "__all__"

    def validate(self, data):
        validated_data = super().validate(data)
        parent = validated_data.get("parent")
        user = self.context.get("request").user

        categories = Category.objects.filter(
            restaurant__user=user
        )
        if parent not in categories:
            raise ValidationError(
                f"You do not have the access to this category"
            )
        return validated_data
