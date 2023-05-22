from django import forms

class SaveForm(forms.Form):
    D0 = forms.CharField(label='D0', max_length=200)
    data = forms.CharField(label="data", max_length=200)
    uid = forms.CharField(label="uid", max_length=200)

    