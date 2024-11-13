from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from restaurant.serializers import *
from restaurant.models import Restaurant, Category, Subcategory, Dish
from restaurant.utils.filter_backends import CustomFilterBackend
from restaurant.utils import CategoryFilter
from restaurant.utils.permissions import IsTheUserWhoCreated


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return CategoryAllFieldsSerializer
        else:
            return super().get_serializer_class()

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        if self.action == "update" or self.action == "destroy" or self.action == "partial_update":
            return [IsTheUserWhoCreated("category")]
        return super().get_permissions()


class SubcategoryViewSet(ModelViewSet):
    serializer_class = SubcategorySerializer
    queryset = Subcategory.objects.all()
    filterset_class = CategoryFilter
    filter_backends = [CustomFilterBackend]

    def retrieve(self, request, *args, **kwargs):
        qs = Dish.objects.filter(category_id=kwargs.get("pk"))
        qs = CustomFilterBackend().filter_queryset(request, qs, self)
        serializer = DishSerializer(
            qs,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data)

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        if self.action == "update" or self.action == "destroy" or self.action == "partial_update":
            return [IsTheUserWhoCreated("subcategory")]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return SubcategoryAllFieldsSerializer
        else:
            return super().get_serializer_class()


class DishViewSet(ModelViewSet):
    serializer_class = DishSerializer
    queryset = Dish.objects.all()

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        if self.action == "update" or self.action == "destroy" or self.action == "partial_update":
            return [IsTheUserWhoCreated("dish")]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return DishAllFieldsSerializer
        else:
            return super().get_serializer_class()


class RestaurantViewSet(ModelViewSet):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        if self.action == "update" or self.action == "destroy" or self.action == "partial_update":
            return [IsTheUserWhoCreated("restaurant")]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return RestaurantAllFieldsSerializer
        else:
            return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CreateIngredientViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
