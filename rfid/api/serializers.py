from ..models import Esp32, RFID
from rest_framework import serializers

class Esp32Serializer(serializers.ModelSerializer):
    class Meta:
        model = Esp32
        fields = ("id", "user", "unique_id", "timestamp", "mac")
        depth = 1
        
class RFIDsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFID
        fields = ("id", "esp", "uid", "value", "timestamp", "sent_from_server")
        depth = 1