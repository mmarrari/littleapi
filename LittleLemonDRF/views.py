from django.contrib.auth.models import Group, User
from django.db.models import Count
from django.shortcuts import get_object_or_404
from djoser.views import TokenCreateView
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .models import Cart, Category, MenuItem, Order
from .permissions import IsManagerOrAdmin, IsDeliveryCrewOrAdmin
from .serializers import (
    CartSerializer, CategorySerializer, CategoryWithItemsSerializer,
    FullMenuItemSerializer, ManagerMenuItemSerializer, UserSerializer,
    OrderSerializer, OrderDeliveryCrewSerializer
)

class CustomPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 1000

@api_view(['POST','GET'])
@permission_classes([IsAdminUser])
def managers(request):
    if request.method == 'POST':
        username = request.data.get('username')
        if username:
            user = get_object_or_404(User, username=username)
            manager_group = Group.objects.get(name="Manager")
            manager_group.user_set.add(user)
            return Response({"message": "User added in Manager Group"}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        manager_group = Group.objects.get(name="Manager")
        manager_users = User.objects.filter(groups=manager_group)
        serializer = UserSerializer(manager_users, many=True)
        return Response(serializer.data)
    return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_manager(request, user_id):
    user = get_object_or_404(User, id=user_id)
    managers_group = Group.objects.get(name="Manager")
    managers_group.user_set.remove(user)
    return Response({"message": "DELETE Success"}, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAdminUser]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

class MenuItemsbyCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.annotate(num_menuitems=Count('menuitems')).filter(num_menuitems__gt=0)
    serializer_class = CategoryWithItemsSerializer
    http_method_names = ['get']
    permission_classes = [IsAuthenticated] 

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    pagination_class = CustomPagination
    filter_backends = [filters.OrderingFilter]
    ordering = ['id']

    def get_permissions(self):
        permission_classes = []
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated] 
        elif self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsAdminUser] 
        elif self.action in ['partial_update']:
            permission_classes = [IsManagerOrAdmin] 
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        user = self.request.user
        action = self.action
        if user.is_superuser:
            return FullMenuItemSerializer
        try:
            manager_group = Group.objects.get(name='Manager')  
        except Group.DoesNotExist:
            manager_group = None

        if manager_group in user.groups.all():
            if action in ['list', 'retrieve']:
                return FullMenuItemSerializer
            else:
                return ManagerMenuItemSerializer

        if user.is_authenticated:
            return FullMenuItemSerializer

        return ManagerMenuItemSerializer


@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def delivery_crew(request):
    is_manager = request.user.groups.filter(name='Manager').exists()
    if request.method == 'POST':
        if is_manager:
            username = request.data.get('username')
            if username:
                user = get_object_or_404(User, username=username)
                delivery_crew_group = Group.objects.get(name="Delivery Crew")
                delivery_crew_group.user_set.add(user)
                return Response({"message": "User added in Delivery Crew Group"})
            else:
                return Response({"message": "You have to provide username"}, status=status.HTTP_400_FORBIDDEN)
        else:
            return Response({"message": "Only Managers can Add a user to a Delivery Crew group"}, status=status.HTTP_403_FORBIDDEN)
    elif request.method == "GET":
        if is_manager:
            delivery_crew_group = Group.objects.get(name="Delivery Crew")
            delivery_crew_users = User.objects.filter(groups=delivery_crew_group)
            serializer = UserSerializer(delivery_crew_users, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "Only Managers can get users from Delivery Crew group"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "error in request"}, status=status.HTTP_400_BAD_REQUEST)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    @action(detail=False, methods=['POST'])
    def add_item(self, request):
        user = request.user
        menu_item_id = request.data.get('menu_item_id')
        quantity = int(request.data.get('quantity', 1))
        
        if menu_item_id is None or quantity is None:
            raise ValidationError("menu_item_id must be provided.")
        
        menu_item = get_object_or_404(MenuItem, id=menu_item_id)
        cart_item = Cart.add_menu_item(user=user, menu_item=menu_item, quantity=quantity)
        
        if cart_item:
            cart = Cart.objects.filter(user=user)
            serializer = CartSerializer(cart, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Unable to add item to cart"}, status=status.HTTP_400_BAD_REQUEST)
        
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get_permissions(self):
        permission_classes = []
        
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated] 
        elif self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsManagerOrAdmin] 
        elif self.action in ['partial_update']:
            permission_classes = [IsDeliveryCrewOrAdmin] 
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        user = self.request.user
        action = self.action
        if user.is_superuser:
            return OrderSerializer
        try:
            delivery_crew_group = Group.objects.get(name='Delivery Crew')  
        except Group.DoesNotExist:
            delivery_crew_group = None

        if delivery_crew_group in user.groups.all():
            if action in ['list', 'retrieve']:
                return OrderSerializer
            else:
                return OrderDeliveryCrewSerializer

        return OrderSerializer
    
    @action(detail=True, methods=['POST'])
    def assign_delivery_crew(self, request, pk=None):
        user = request.user

        if not (user.is_superuser or user.groups.filter(name="Manager").exists()):
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        order = self.get_object()
        delivery_crew_id = request.data.get('delivery_crew', None)

        if delivery_crew_id is None:
            return Response({"error": "No delivery_crew provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            delivery_crew = User.objects.get(id=delivery_crew_id)
        except User.DoesNotExist:
            return Response({"error": "Invalid delivery_crew_id"}, status=status.HTTP_400_BAD_REQUEST)

        if not delivery_crew.groups.filter(name='Delivery Crew').exists():
            return Response({"error": "User is not part of Delivery Crew"}, status=status.HTTP_400_BAD_REQUEST)

        order.delivery_crew = delivery_crew
        order.save()

        order_serializer = OrderSerializer(order)
        return Response({"message": "Delivery crew assigned successfully", "order": order_serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def create_from_cart(self, request):
        user = request.user
        new_order = Order.create_order_from_cart(user)
        
        if new_order:
            serializer = OrderSerializer(new_order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "No items in cart"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'],permission_classes=[IsDeliveryCrewOrAdmin])
    def deliverycrew(self, request):
        user = request.user
        if user.id is not None:
            if not user.groups.filter(name='Delivery Crew').exists():
                return Response({"error": "User is not part of Delivery Crew"}, status=status.HTTP_400_BAD_REQUEST)
            delivery_crew_orders = Order.objects.filter(delivery_crew=user.id)
            serializer = OrderSerializer(delivery_crew_orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User have to be authenticated"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except:
            return Response({"detail": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Order deleted successfully"}, status=status.HTTP_200_OK)
