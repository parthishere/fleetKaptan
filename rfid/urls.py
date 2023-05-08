from django.urls import path, include
from .views import home

urlpatterns = [
    path("home/<str:esp_name>",home),
]