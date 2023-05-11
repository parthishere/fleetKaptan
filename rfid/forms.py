from django import forms

from .models import Esp32

class EspForm(forms.ModelForm):
    class Meta:
        model = Esp32
        fields = ("__all__")