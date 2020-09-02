from django.urls import path, include

from .views import minio_file_save_view, s3_file_save_view


urlpatterns = [
    path('minio/', include([
        path('file/save/', minio_file_save_view),
    ])),
    path('s3/', include([
        path('file/save/', s3_file_save_view),
    ])),
]
