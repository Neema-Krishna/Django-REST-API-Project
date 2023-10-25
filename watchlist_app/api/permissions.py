from rest_framework import permissions


class AdminOrReadonly(permissions.IsAdminUser):
    def has_permission(self,request,view):
        # admin_permission=bool(request.user and request.user.is_staff)
        if request.method in permissions.SAFE_METHODS:
            return True
    # Check permissions for read-only request
        else:
            return bool(request.user and request.user.is_staff)
    # Check permissions for write request
         
    
class Review_userOrReadonly(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:
            return True
    # Check permissions for read-only request
        else:
            return obj.user_name==request.user or request.user.is_admin
    # Check permissions for write request
        