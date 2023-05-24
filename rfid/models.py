from django.db import models
from datetime import timezone

from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

import random
import string




def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_id_generator_esp(instance):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
        """
    new_id = random_string_generator(size=12)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(unique_id=new_id).exists()
    print(instance.__class__)
    if qs_exists:
        new_slug = "esp-{randstr}".format(
                    randstr=random_string_generator(size=12)
                )
        return new_slug
    else:
        return new_id
    


class Esp32Manager(models.Manager):
    def get_or_new(self, mac=None):
        qs = self.get_queryset().filter(mac_unhashed=mac)
        
        if qs.exists():
            obj = qs.first()
        else:
            obj = self.new(mac=mac)
            
    def new(self, mac=None):
        obj = self.model.objects.create(mac_unhashed=mac)
        return obj
        
        
class Esp32(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='esps')
    unique_id = models.CharField(null=True, blank=True, max_length=120) 
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    mac = models.CharField(max_length=50, null=True, blank=True) 
    objects = Esp32Manager()
    
    def __str__(self):
        return f"esp {str(self.pk)}"
    
    def get_absolute_url(self):
        return reverse("rfid:detail-esp", kwargs={"esp_name": self.unique_id})
    
    
    
class RFID(models.Model):
    esp = models.ForeignKey(Esp32, on_delete=models.CASCADE, related_name='rfids')
    boolean_val = models.BooleanField(default=True)
    uid = models.CharField(default='id', max_length=120)
    value = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    sent_from_server=models.BooleanField(default=True)
    
    def __str__(self):
        return str(f"applience of {self.esp.unique_id} : {self.pk}")
    
def esp_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.unique_id == None or instance.unique_id == "" or instance.pk==None:
        instance.unique_id = unique_id_generator_esp(instance)
            

pre_save.connect(esp_pre_save_receiver, sender=Esp32)

    
def user_post_save_receiver(sender, instance, *args, **kwargs):
    try:
        obj = Esp32.objects.get(user=instance)
        if obj is None:
            Esp32.objects.create(user=instance)
        else:
            pass
    except:
         Esp32.objects.create(user=instance)
post_save.connect(user_post_save_receiver, sender=User)


    
    
    
    
