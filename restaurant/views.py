from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin, DestroyModelMixin
)
from restaurant.serializers import *
from restaurant.models import Restaurant, Category, Subcategory, Menu, Dish
from restaurant.utils.filter_backends import CustomFilterBackend
from restaurant.utils import CategoryFilter


class CategoryViewSet(ListModelMixin, GenericViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class SubcategoryViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
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


class RestaurantViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        return super().get_permissions()


class MenuViewSet(CreateModelMixin,
                  ListModelMixin,
                  UpdateModelMixin,
                  GenericViewSet):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == "list":
            return []
        else:
            return super().get_permissions()
