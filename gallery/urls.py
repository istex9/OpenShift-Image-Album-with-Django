from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_photo, name='upload_photo'),
    path('delete/<int:photo_id>/', views.delete_photo, name='delete_photo'),
    path('photo/<int:photo_id>/', views.photo_detail, name='photo_detail'),
]
