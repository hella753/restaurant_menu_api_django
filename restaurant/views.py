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

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            queryset = Category.objects.select_related(
                "restaurant",
                "restaurant__user"
            )
        else:
            queryset = Category.objects.filter(
                restaurant__user=self.request.user
            ).select_related(
                "restaurant",
                "restaurant__user"
            )
        return queryset

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return CategoryAllFieldsSerializer
        else:
            return super().get_serializer_class()

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        elif (
                self.action == "update" or
                self.action == "destroy" or
                self.action == "partial_update"
        ):
            return [IsTheUserWhoCreated("category")]
        else:
            return super().get_permissions()


class SubcategoryViewSet(ModelViewSet):
    serializer_class = SubcategorySerializer
    filterset_class = CategoryFilter
    filter_backends = [CustomFilterBackend]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            queryset = Subcategory.objects.select_related(
                "parent",
                "parent__restaurant",
                "parent__restaurant__user",
            )
        else:
            queryset = Subcategory.objects.filter(
                parent__restaurant__user=self.request.user
            ).select_related(
                "parent",
                "parent__restaurant",
                "parent__restaurant__user",
            )
        return queryset

    def retrieve(self, request, *args, **kwargs):
        qs = Dish.objects.prefetch_related(
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

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        elif (
                self.action == "update" or
                self.action == "destroy" or
                self.action == "partial_update"
        ):
            return [IsTheUserWhoCreated("subcategory")]
        else:
            return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return SubcategoryAllFieldsSerializer
        else:
            return super().get_serializer_class()


class DishViewSet(ModelViewSet):
    serializer_class = DishSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            queryset = Dish.objects.select_related(
                "category",
                "category__parent",
                "category__parent__restaurant",
                "category__parent__restaurant__user",
            )
        else:
            queryset = Dish.objects.filter(
                category__parent__restaurant__user=self.request.user
            ).select_related(
                "category",
                "category__parent",
                "category__parent__restaurant",
                "category__parent__restaurant__user",
            )
        return queryset

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        elif (
                self.action == "update" or
                self.action == "destroy" or
                self.action == "partial_update"
        ):
            return [IsTheUserWhoCreated("dish")]
        else:
            return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return DishAllFieldsSerializer
        else:
            return super().get_serializer_class()


class RestaurantViewSet(ModelViewSet):
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            queryset = Restaurant.objects.select_related(
                "user"
            )
        else:
            queryset = Restaurant.objects.filter(
                user=self.request.user
            ).select_related(
                "user"
            )
        return queryset

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return RestaurantAllFieldsSerializer
        else:
            return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        elif (
                self.action == "update" or
                self.action == "destroy" or
                self.action == "partial_update"
        ):
            return [IsTheUserWhoCreated("restaurant")]
        else:
            return super().get_permissions()


class CreateIngredientViewSet(CreateModelMixin,
                              DestroyModelMixin,
                              GenericViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        elif self.action == "destroy":
            return [IsTheUserWhoCreated("ingredient")]
        else:
            return super().get_permissions()
