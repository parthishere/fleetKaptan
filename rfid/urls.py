from django.urls import path, include
from .views import home

urlpatterns = [
    path("socket/<str:esp_name>",home),
]