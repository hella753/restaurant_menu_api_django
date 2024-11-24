from rest_framework.routers import DefaultRouter
from restaurant.views import *

app_name = "restaurant"

router = DefaultRouter()
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'subcategory', SubcategoryViewSet, basename='subcategory')
router.register(r'restaurants', RestaurantViewSet, basename='restaurants')
router.register(r'dish', DishViewSet, basename='dish')
urlpatterns = router.urls
