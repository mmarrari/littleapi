from django.contrib import admin
from .models import (
    MenuItem,
    Category,
    Cart,
    Order,
    OrderItem
)
# Register your models here.

admin.site.register((MenuItem,Category,Cart,Order,OrderItem))