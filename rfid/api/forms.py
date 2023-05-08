from django import forms

class SaveForm(forms.Form):
    password = forms.CharField(label='password', max_length=200)
    D0 = forms.CharField(label='D0', max_length=200)
    D1 = forms.CharField(label='D1', max_length=200)
    D2 = forms.CharField(label='D2', max_length=200)
    D3 = forms.CharField(label='D3', max_length=200)
    D4 = forms.CharField(label='D4', max_length=200)
    A0 = forms.CharField(label='A0', max_length=200)
    username = forms.CharField(label='username', max_length=200)
    uqid = forms.CharField(label='uqid', max_length=200)
    