from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AlbumViewSet, PhotoViewSet

router = DefaultRouter()
router.register(r"albums", AlbumViewSet, basename="album")
router.register(r"photos", PhotoViewSet, basename="photo")

urlpatterns = [
    path("", include(router.urls)),
]
