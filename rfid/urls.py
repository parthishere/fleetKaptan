from django.urls import path, include
from .views import home, list_esps, detail_esp, create_esp, update_esp, delete_esp, delete_rfid


app_name = "rfid"
urlpatterns = [
    path("socket/<str:esp_name>",home,name="home"),
    
    path("list/",list_esps,name="esp-list"),
    path("create-esp/",create_esp,name="create-esp"),
    path("esp/<str:esp_name>",detail_esp,name="detail-esp"),
    path("esp/<str:esp_name>/update",update_esp,name="update-esp"),
    path("esp/<str:esp_name>/delete",delete_esp,name="delete-esp"),
    
    path("rfid/<str:unique_id>/<int:pk>/delete",delete_rfid,name="delete-rfid"),
]