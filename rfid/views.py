from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
# Create your views here.
def home(request, esp_name):
    
    return render(request, "home.html", {"esp_name":esp_name})

