from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import User

from .models import Album, Photo
from .permissions import IsOwnerOrReadOnly
from .serializers import AlbumSerializer, BulkPhotoSerializer, PhotoSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.filter(is_deleted=False)
    serializer_class = AlbumSerializer
    permission_classes = [IsOwnerOrReadOnly]

    @action(detail=True, methods=["post"], url_path="add-photo")
    def add_photo(self, request, pk=None):
        album = self.get_object()
        photo_id = request.data.get("photo_id")
        try:
            photo = Photo.objects.get(id=photo_id)
            album.photos.add(photo)
            return Response(
                {"message": "Photo added to album."}, status=status.HTTP_200_OK
            )
        except Photo.DoesNotExist:
            return Response(
                {"error": "Photo not found."}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=["post"], url_path="remove-photo")
    def remove_photo(self, request, pk=None):
        album = self.get_object()
        photo_id = request.data.get("photo_id")
        try:
            photo = Photo.objects.get(id=photo_id)
            album.photos.remove(photo)
            return Response(
                {"message": "Photo removed from album."}, status=status.HTTP_200_OK
            )
        except Photo.DoesNotExist:
            return Response(
                {"error": "Photo not found."}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=["post"], url_path="bulk-upload-photos")
    def bulk_upload_photos_in_album(self, request, pk=None):
        album = self.get_object()
        serializer = BulkPhotoSerializer(
            data=request.data,
            many=True,
            context={"album": album, "action": "upload", "request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Photos uploaded and added to the album successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"], url_path="bulk-assign-photos")
    def bulk_assign_photos_to_album(self, request, pk=None):
        album = self.get_object()
        photo_ids = request.data.get("photo_ids", [])
        photos = Photo.objects.filter(id__in=photo_ids)
        if len(photo_ids) != photos.count():
            return Response(
                {"error": "Some photo IDs are invalid."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        album.photos.add(*photos)
        return Response(
            {"message": "Photos assigned to the album successfully."},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"], url_path="bulk-remove-photos")
    def bulk_remove_photos_from_album(self, request, pk=None):
        album = self.get_object()
        photo_ids = request.data.get("photo_ids", [])
        photos = Photo.objects.filter(id__in=photo_ids)
        if len(photo_ids) != photos.count():
            return Response(
                {"error": "Some photo IDs are invalid."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        album.photos.remove(*photos)
        return Response(
            {"message": "Photos removed from the album successfully."},
            status=status.HTTP_200_OK,
        )


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.filter(is_deleted=False)
    serializer_class = PhotoSerializer
    permission_classes = [IsOwnerOrReadOnly]

    @action(detail=True, methods=["post"])
    def share(self, request, pk=None):
        photo = self.get_object()
        viewer_ids = request.data.get("viewers", [])
        viewers = User.objects.filter(id__in=viewer_ids)
        photo.viewers.add(*viewers)
        return Response(
            {"message": "Photo shared successfully."}, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["post"], url_path="bulk-upload")
    def bulk_upload_photos(self, request):
        serializer = BulkPhotoSerializer(
            data=request.data,
            many=True,
            context={"action": "upload", "request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Photos uploaded successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
