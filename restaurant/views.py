from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from restaurant.serializers import *
from restaurant.models import Restaurant, Category, Subcategory, Dish
from restaurant.utils.filter_backends import CustomFilterBackend
from restaurant.utils import CategoryFilter
from restaurant.utils.permissions_v2 import IsOwnerOrReadOnly


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.select_related(
        "restaurant",
    )
    user_lookup = "restaurant__user"

    def get_serializer_class(self):
        if self.action != "list" or self.action != "retrieve":
            return CategoryAllFieldsSerializer
        else:
            return super().get_serializer_class()

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        else:
            return [IsOwnerOrReadOnly()]


class SubcategoryViewSet(ModelViewSet):
    serializer_class = SubcategorySerializer
    queryset = Subcategory.objects.select_related(
        "parent"
    )
    filterset_class = CategoryFilter
    filter_backends = [CustomFilterBackend]
    user_lookup = "parent__restaurant__user"

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        else:
            return [IsOwnerOrReadOnly()]

    def retrieve(self, request, *args, **kwargs):
        subcategory_object = Subcategory.objects.filter(
            pk=kwargs["pk"]
        ).first()
        self.check_object_permissions(self.request, subcategory_object)
        qs = Dish.objects.select_related(
            "category",
        ).prefetch_related(
            "ingredients"
        ).filter(
            category_id=kwargs.get("pk")
        )
        qs = CustomFilterBackend().filter_queryset(request, qs, self)
        serializer = DishSerializer(
            qs,
            many=True,
            context={"request": request}
        )
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action != "list" or self.action != "retrieve":
            return SubcategoryAllFieldsSerializer
        else:
            return super().get_serializer_class()


class DishViewSet(ModelViewSet):
    serializer_class = DishSerializer
    queryset = Dish.objects.select_related(
        "category"
    ).prefetch_related(
        "ingredients"
    )
    user_lookup = "category__parent__restaurant__user"

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        else:
            return [IsOwnerOrReadOnly()]

    def get_serializer_class(self):
        if self.action != "list" or self.action != "retrieve":
            return DishAllFieldsSerializer
        else:
            return super().get_serializer_class()


class RestaurantViewSet(ModelViewSet):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.select_related("user")
    user_lookup = "user"

    def get_serializer_class(self):
        if self.action != "list" or self.action != "retrieve":
            return RestaurantAllFieldsSerializer
        else:
            return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        else:
            return [IsOwnerOrReadOnly()]
