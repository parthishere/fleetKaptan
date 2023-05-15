from django import forms

from .models import Esp32, RFID

class EspForm(forms.ModelForm):
    class Meta:
        model = Esp32
        fields = ("__all__")
        
class RFIDForm(forms.ModelForm):
    class Meta:
        model = RFID
        fields = ("value",)
    def __init__(self, *args, **kwargs):
        super(RFIDForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'