from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class Esp32ListCreateView(ListCreateAPIView):
    serializers_class = Esp32Serializer
    queryset = Esp32.objects.all()
    
    