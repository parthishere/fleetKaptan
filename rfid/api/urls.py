
from django.urls import path, include
from .views import ESPListCreateAPI, ESPRetriveUpdateDestroyAPIView, return_data_to_esp_view, get_posted_data_from_esp

app_name = "rfid-api"

urlpatterns = [
    path("esp-list", ESPListCreateAPI.as_view(), name="list-esp"),
    path("<str:unique_id>", ESPRetriveUpdateDestroyAPIView.as_view(), name="detail-esp"),
    
    path("write-to-rfid/", return_data_to_esp_view, name="list-rfid"),
    path("<str:unique_id>/read-esp-scanned", get_posted_data_from_esp, name="detail-rfid"),
]
    
    