from django.urls import path
from . import views

urlpatterns = [
    path('/gallery/', views.home, name='home'),
    path('/gallery/upload/', views.upload_photo, name='upload_photo'),
    path('/gallery/delete/<int:photo_id>/', views.delete_photo, name='delete_photo'),
    path('/gallery/photo/<int:photo_id>/', views.photo_detail, name='photo_detail'),
]
