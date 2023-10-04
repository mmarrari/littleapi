from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'category', views.CategoryViewSet, basename="")
router.register(r'menu-item', views.MenuItemViewSet, basename="")
router.register(r'menu-item-by-category', views.MenuItemsbyCategoryViewSet, basename="")
router.register(r'cart', views.CartViewSet)
router.register(r'order', views.OrderViewSet)

urlpatterns = [
    path('groups/manager/users', views.managers, name='managers'),
    path('groups/manager/users/<int:user_id>', views.delete_manager, name='delete-manager'),
    path('groups/delivery-crew/users', views.delivery_crew),
    path('', include(router.urls)),
]