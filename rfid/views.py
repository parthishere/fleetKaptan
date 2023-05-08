from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView

from .models import Esp32, RFID

# Create your views here.
def home(request, esp_name):
    
    return render(request, "home.html", {"esp_name":esp_name})

@login_required
def list_esps(request):
    context = {}
    user = request.user
    esps = Esp32.objects.filter(user=user)
    context['esp_list'] = esps
    return render(request, "rfid/list-esp.html", context)


@login_required 
def create_esp(request):
    context = {}
    
    user = request.user
    esps = Esp32.objects.filter(user=user)
    esp_count = esps.count()
    
    form = EspForm(request.POST or None)
    
    context['form'] = form
    
    if request.POST and form.is_valid():
        
        esp_instance = form.save(commit=False)
        esp_instance.created_by = user
        esp_instance.save()
        context['form'] = form
        return redirect(esp_instance.get_absolute_url)
        
    return render(request, "rfid/create-esp.html", context)


@login_required 
def detail_esp(request, pk=None):
    context = {}
    esp_instance = Esp32.objects.select_related("user").prefetch_related("rfids").get(pk=pk, removed=False)
    if request.user == esp_instance.user:
        context['esp_detail'] = esp_instance
    else:
        return redirect("home")
    return render(request, "esps/detail-esp.html", context)

@login_required 
def update_esp(request, pk=None):
    context = {}
    user = request.user
    esp_instance = Esp32.objects.exclude(removed=True).get(pk=pk)
    
    form = EspForm(request.POST or None, instance=esp_instance)
    
    context['form'] = form
    
    if request.POST and user is esp_instance.user:
        
        esp_instance = form.save(commit=False)
        esp_instance.user = user
    
        esp_instance.save()
        context['form'] = form
        return redirect(esp_instance.get_absolute_url)
 
    return render(request, "esps/create-esp.html", context)
        
   
@login_required  
def delete_esp(request, pk=None):
    user = request.user
    esp_instance = Esp32.objects.get(pk=pk)
  
    if user == esp_instance.created_by:
        esp_instance.delete()
        esp_instance.save()
        return redirect("esps:list")
    
    return redirect(esp_instance.get_absolute_url)