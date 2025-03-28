storing photos locally, app to manage, share photos (google photos)

MVP
> Storage medium for storing photos
> Retrieve photos at any time
> My photos should not be able to be accessed by other people
> Share the photos
> Group the photos by any category - wedding, ceremony, albums
> User can upload and view photos/ albums at any time, any place, (no restricts on uploading and viewing own photos)



Albums(id, name, description, cover_photo, album_owner, album_viewers)
class Album():
-id
-description
-name
-cover_photo (string)
-album_owner - models.ForeignKey(User, on_delete = models.CASCADE)
-album_viewers - models.M2MField


Photos(id, tag, album_id, owner, uploaded_time)
-id
-tag (string) - wedding in kathmandu
-albums (ManyToManyField(Album))
-photo_viewers (M2MField)
-owner(User)
-uploaded_time
-url(string)
-is_deleted (bool)


-api/resource(url)
-http method
-payload (optional)
-response (message, status, error(optional))

1. Upload album
METHOD: post
API: /api/v1/album
PAYLOAD:
{
    description(optional), name, cover_photo(optional)
}
RESPONSE:
{
    message: "Album has been created",
    data: {
        'album_id': id,
        'name',
        'description'
        ...
    },
    error: None
}

2. List albums - /api/v1/albums [GET]
3. Retrieve album - /api/v1/album/{id} [GET] - is_deleted = False
{
    'album_id': id,
        'name',
        'description',
        photos: [
            {
                id
                name
                url
                ...
            }
            {
                id
                name
                url
                ...
            },
        ]

}
4. Delete album - /api/v1/album/{id} [DELETE]

5. Upload a single photo [CRUD]
METHOD: post
API: /api/v1/photo
PAYLOAD:
{
    photo(blob/file)
}



6. Upload photo to an album
METHOD: post
API: /api/v1/album/{id}/photo
PAYLOAD:
{
    photo(blob/file)
}

7. Get specific photo from an album
/api/v1/album/{id}/photo/{id} - [GET]

8. Remove/Update particular photo from an album
API: /api/v1/album/{id}/photo/{id}
Payload for update - PATCH
{
    photo(blob/file)
}
Delete - no payload - DELETE

9. Remove from an album - PATCH
/api/v1/album/{id}/remove-photo/{id}
remove album_id from particular photo

4. Bulk upload
METHOD: post
API: /api/v1/album/{id}/photos
PAYLOAD:
{
    photos1(blob/file),
    photos2(blob/file),
    ...
}


10. Share photo
/api/v1/photo/{id}/share
- add photo_viewers from payload
{
    viewers: [user_id1, user_id2]
}





+19196270162