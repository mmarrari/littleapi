from rest_framework import permissions
from django.contrib.auth.models import Group

class IsManagerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        try:
            manager_group = Group.objects.get(name='Manager')  
        except Group.DoesNotExist:
            manager_group = None
        if manager_group in request.user.groups.all():
            return True
        if request.user.is_superuser:
            return True
        
        return False

class IsDeliveryCrewOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        try:
            deliverycrew_group = Group.objects.get(name='Delivery Crew')  
        except Group.DoesNotExist:
            deliverycrew_group = None
        if deliverycrew_group in request.user.groups.all():
            return True
        if request.user.is_superuser:
            return True
        return False