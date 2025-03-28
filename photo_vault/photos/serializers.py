from rest_framework import serializers
from users.serializers import UserProfileSerializer as UserSerializer

from .models import Album, Photo


class PhotoSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    viewers = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Photo
        fields = [
            "id",
            "image_url",
            "albums",
            "viewers",
            "owner",
            "uploaded_time",
            "is_deleted",
        ]
        read_only_fields = ["id", "owner", "uploaded_time", "is_deleted"]

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


class AlbumSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    viewers = UserSerializer(many=True, read_only=True)
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = [
            "id",
            "name",
            "description",
            "cover_photo",
            "owner",
            "viewers",
            "created_at",
            "updated_at",
            "is_deleted",
        ]
        read_only_fields = ["id", "owner", "created_at", "updated_at", "is_deleted"]

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


class BulkPhotoSerializer(serializers.Serializer):
    id = serializers.UUIDField(
        required=False
    )  # Used for assigning to and removing from an album
    image_url = serializers.URLField(required=False)  # Used for uploading

    def validate(self, data):
        if self.context.get("action") == "upload" and not data.get("image_url"):
            raise serializers.ValidationError(
                {"image_url": "This field is required for uploads."}
            )
        return data

    def create(self, validated_data):
        album = self.context.get("album")
        photo = Photo.objects.create(
            image_url=validated_data["image_url"],
            owner=self.context["request"].user,
        )
        if album:
            photo.albums.add(album)
        return photo
