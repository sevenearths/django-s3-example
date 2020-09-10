from django.urls import path, include

from .views import minio_file_save_view, boto3_file_save_view


urlpatterns = [
    path('minio/file/save/', minio_file_save_view),
    path('boto3/file/save/', boto3_file_save_view),
]
