from django.contrib.auth.models import User
from .models import MenuItem, Category, Cart, Order, OrderItem
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'first_name', 'last_name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class FullMenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']

class ManagerMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['featured']

class SimpleMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured']

class CategoryWithItemsSerializer(serializers.ModelSerializer):
    menuitems = SimpleMenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'menuitems']

class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    menuitem = FullMenuItemSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ('user', 'menuitem', 'quantity', 'unit_price', 'price')

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ('title', 'featured', 'category')

class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'menuitem', 'quantity', 'unit_price', 'price')
        unique_together = ('order', 'menuitem')

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ('id', 'user', 'delivery_crew', 'status', 'total', 'date', 'order_items')

class OrderDeliveryCrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']