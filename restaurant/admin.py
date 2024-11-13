from django.contrib import admin
from restaurant.models import *


admin.site.register(Restaurant)
admin.site.register(Dish)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Ingredient)
