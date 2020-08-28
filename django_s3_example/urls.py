from django.urls import path, include

from .views import minio_file_save_view, minio_file_load_view


urlpatterns = [
    path('minio/', include([
        path('file/', include([
            path('save/', minio_file_save_view),
            path('load/', minio_file_load_view),
        ])),
    ])),
]
