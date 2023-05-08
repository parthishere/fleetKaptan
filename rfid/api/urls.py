
from django.urls import path, include
from .views import ESPListCreateAPI, ESPRetriveUpdateDestroyAPIView, return_data_to_esp_view, get_posted_data_from_esp


urlpatterns = [
    path("", ESPListCreateAPI.as_view(), name="list-esp"),
    path("<str:unique_id>", ESPRetriveUpdateDestroyAPIView.as_view(), name="detail-esp"),
    
    path("", return_data_to_esp_view, name="list-rfid"),
    path("<str:unique_id>", get_posted_data_from_esp, name="detail-rfid"),
]
    
    