from rest_framework.permissions import BasePermission

from .models import Album, Photo


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and obj.owner == request.user:
            return True

        if request.method in ["GET", "HEAD", "OPTIONS"]:
            if isinstance(obj, Album):
                return request.user in obj.viewers.all()
            elif isinstance(obj, Photo):
                return request.user in obj.viewers.all()

        return False
