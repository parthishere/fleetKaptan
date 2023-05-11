from django import forms

class SaveForm(forms.Form):
    password = forms.CharField(label='password', max_length=200)
    D0 = forms.CharField(label='D0', max_length=200)
    data = forms.CharField(label="data", max_length=200)
    username = forms.CharField(label='username', max_length=200)
    uqid = forms.CharField(label='uqid', max_length=200)
    