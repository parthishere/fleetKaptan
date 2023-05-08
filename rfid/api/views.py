from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import Esp32Serializer, RFIDsSerializer
from ..models import Esp32, RFID
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import SaveForm

class ESPListCreateAPI(ListCreateAPIView):
    queryset = Esp32.objects.all()
    serializer_class = Esp32Serializer
    permission_classes = [IsAuthenticated,]
    lookup_field = ['unique_id']
    lookup_url_kwarg = ['unique_id']
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def list(self, request):
        queryset = self.get_queryset().filter(user=request.user)
        serializer = Esp32Serializer(queryset, many=True)
        return Response(serializer.data)
    
class ESPRetriveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Esp32.objects.all()
    serializer_class = Esp32Serializer
    permission_classes = [IsAuthenticated]
    lookup_field= "unique_id"
    
    
    def perform_update(self, serializer):
        instance = serializer.save(user=self.request.user.user_profile)
        
    def perform_destroy(self, instance):
        if self.request.user == instance.user:
            instance.delete()
        

@api_view(['GET'])
def return_data_to_esp_view(request):
    message = {}
    username = request.query_params.get('username')
    unique_id = request.query_params["uqid"]
    
    unique_id.replace(" ", "")
    uqid = ""
    for a in unique_id:
        if a == '\0' or a == "" or len(a) == 0:
            pass
        else:
            uqid += a

    try:
        esp = Esp32.objects.get(user__username=username, unique_id=uqid)
        
        appliences = RFID.objects.filter(esp=esp).order_by("-id")
    except:
        message = {"error": "404", "data": "Object not found !"}
        return Response(message)
    
    serializer = RFIDsSerializer(appliences, many=True)
    print(Response(serializer.data))
    return Response(serializer.data)

from django.views.decorators.csrf import csrf_exempt


@api_view(['POST', 'PUT', 'PATCH'])
@csrf_exempt
def get_posted_data_from_esp(request):
    message = {}
    appliences = None
    form = SaveForm(request.POST)
    form.is_valid()
    
    unique_id = request.query_params.get('uqid').strip()
    username = request.query_params.get('username').strip()
    
    unique_id.replace(" ", "")
    uqid = ""
    for a in unique_id:
        if a == '\0' or a == "" or len(a) == 0:
            pass
        else:
            uqid += a
    
    password = form.cleaned_data.get('password')
    D0 = form.cleaned_data.get('D0')
    D1 = form.cleaned_data.get('D1')
    D2 = form.cleaned_data.get('D2')
    D3 = form.cleaned_data.get('D3')
    D4 = form.cleaned_data.get('D4')
    D5 = form.cleaned_data.get('D5')
    A0 = form.cleaned_data.get('A0')
    
    try:
        esp = Esp32.objects.get(user__user__username=username, unique_id=uqid)
        
        appliences = RFID.objects.filter(esp=esp).order_by("-id")
        appliences = RFIDsSerializer(appliences, many=True).data
    except:
        message = {"error": "404", "data": "Object not found !"}
        return Response(message)
    
    
    print(appliences)
    return Response(appliences)
    