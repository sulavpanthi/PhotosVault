import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class Album(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(null=True, blank=True)
    cover_photo = models.CharField(max_length=1024, null=True, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_albums"
    )
    viewers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="shared_albums", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image_url = models.CharField(
        max_length=1024,
    )
    albums = models.ManyToManyField(Album, related_name="photos", blank=True)
    viewers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="shared_photos", blank=True
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_photos"
    )
    uploaded_time = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ["-uploaded_time"]

    def __str__(self):
        return self.image_url
