from django.urls import path, include

from .views import file_save_view, file_load_view


urlpatterns = [
    path('file/', include([
        path('save/', file_save_view),
        path('load/', file_load_view),
    ])),
]
