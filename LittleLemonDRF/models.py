import datetime

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)
    
    def __str__(self):
        return f"{self.id} - {self.title}"
        

class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, related_name='menuitems', on_delete=models.PROTECT)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    class Meta:
        unique_together = ('menuitem','user')

    @classmethod
    def add_menu_item(cls, user, menu_item, quantity):
        cart_item, created = cls.objects.get_or_create(
            user=user, menuitem=menu_item,
            defaults={
                'quantity': 0,
                'unit_price': menu_item.price,
                'price': 0  
            }
        )
        
        cart_item.quantity += quantity
        cart_item.price = cart_item.unit_price * cart_item.quantity
        cart_item.save()
        return cart_item
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="delivery_crew", null=True)
    status = models.BooleanField(db_index=True, default=False)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(db_index=True)

    @classmethod
    def create_order_from_cart(cls, user):
        cart_items = Cart.objects.filter(user=user)
        if not cart_items.exists():
            return None
        total_price = sum(item.price for item in cart_items)
        
        order = cls.objects.create(
            user=user,
            total=total_price,
            date=datetime.date.today()
        )
        
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                menuitem=cart_item.menuitem,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                price=cart_item.price
            )
        
        cart_items.delete()
        return order


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('order','menuitem')
    
