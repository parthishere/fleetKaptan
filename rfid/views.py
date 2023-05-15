from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from django.contrib.auth.decorators import login_required
from .models import Esp32, RFID
from .forms import EspForm, RFIDForm

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
    
    form = EspForm(request.POST or None)
    
    context['form'] = form
    
    if request.POST and form.is_valid():
        
        esp_instance = form.save(commit=False)
        esp_instance.created_by = user
        esp_instance.save()
        context['form'] = form
        return redirect("rfid:esp-list")
        
    return render(request, "rfid/esp-form.html", context)


@login_required 
def detail_esp(request, esp_name=None):
    context = {}
    esp_instance = Esp32.objects.select_related("user").prefetch_related("rfids").get(unique_id=esp_name)
    form = RFIDForm(request.POST or None)
    context["form"] = form
    if request.POST and form.is_valid:
        a = form.save(commit=False)
        a.esp =esp_instance
        a.boolean_value = False
        a.save()
        context["form"] = form
        return redirect(reverse("rfid:detail-esp", kwargs={"esp_name":esp_name}))
    if request.user == esp_instance.user:
        context['esp_detail'] = esp_instance  
    else:
        return redirect("home")
    return render(request, "rfid/detail-esp.html", context)

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
        return redirect(reverse(esp_instance.get_absolute_url))
 
    return render(request, "rfid/esp-form.html", context)
        
   
@login_required  
def delete_esp(request, esp_name=None):
    user = request.user
    esp_instance = Esp32.objects.get(unique_id=esp_name)
  
    if user == esp_instance.user:
        esp_instance.delete()
        return redirect("rfid:esp-list")
    
    return redirect(reverse("rfid:esp-list"))

@login_required  
def delete_rfid(request, unique_id=None, pk=None):
    user = request.user
    esp_instance = Esp32.objects.get(unique_id=unique_id)
    rfid_instance = RFID.objects.get(pk=pk)
  
    if user == esp_instance.user and rfid_instance in esp_instance.rfids.all():
        rfid_instance.delete()
        return redirect("rfid:esp-list")
    
    return redirect(reverse("rfid:detail-esp", kwargs={"esp_name":unique_id}))

