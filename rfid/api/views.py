from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import Esp32Serializer, RFIDsSerializer
from ..models import Esp32, RFID
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import SaveForm
from django.contrib.auth.decorators import login_required

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
            
from django.views.decorators.csrf import csrf_exempt       

@api_view(['GET'])
@login_required
@csrf_exempt
def return_data_to_esp_view(request, unique_id, username):
    message = {}
    
    
    unique_id.replace(" ", "")
    uqid = ""
    usrname=""
    for a in unique_id:
        if a == '\0' or a == "" or len(a) == 0:
            pass
        else:
            uqid += a
            
    for b in username:
        if b == '\0' or b == "" or len(b) == 0:
            pass
        else:
            usrname += b

    try:
        esp = Esp32.objects.get(user__username=usrname, unique_id=uqid)
        
        appliences = RFID.objects.filter(esp=esp).order_by("-id").first()
    except:
        message = {"error": "404", "data": "Object not found !"}
        return Response(message)
    
    serializer = RFIDsSerializer(appliences)
    print(Response(serializer.data))
    return Response(serializer.data)




@api_view(['POST', 'PUT', 'PATCH'])
@csrf_exempt
def get_posted_data_from_esp(request, unique_id, username):
    message = {}
    rfid=None
    form = SaveForm(request.POST)
    form.is_valid()
    
    # unique_id = request.query_params.get('uqid').strip()
    # username = request.query_params.get('username').strip()
    
    unique_id.replace(" ", "")
    uqid = ""
    usrname=""
    for a in unique_id:
        if a == '\0' or a == "" or len(a) == 0:
            pass
        else:
            uqid += a
            
    for b in username:
        if b == '\0' or b == "" or len(b) == 0:
            pass
        else:
            usrname += b
    
    
    D0 = form.cleaned_data.get('D0')
    data = form.cleaned_data.get('data')
    uid = form.cleaned_data.get('uid')
    print(D0, data, uqid, username)
    try:
        esp = Esp32.objects.get(user__username=username, unique_id=uqid)
        print(esp)
        rfid = RFID.objects.create(esp=esp, boolean_val=True if D0 else False, value=data, uid=uid)
        # rfids = RFID.objects.filter(esp=esp).order_by("-id")
        rfid = RFIDsSerializer(rfid).data
        # print(rfids)
    except Exception as e:
        
        print(e)
        message = {"error": "404", "data": "Object not found !"}
        return Response(message)
    
    
    print(rfid)
    return Response(rfid)
    