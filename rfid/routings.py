from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    ##Use to send RFID data to server though esp32
    re_path(r'ws/rfid/(?P<esp_name>\w+)/write$', consumers.WriteToRFID.as_asgi()),
    
    ##Use to send RFID data to esp32 though server
    re_path(r'ws/rfid/(?P<esp_name>\w+)/read$', consumers.SendRfidDataToESP.as_asgi()),
]
