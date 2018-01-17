from django import forms

from reservations.models import Registration
from django.contrib.auth.forms import AuthenticationForm

class RegistrationCreateForm(forms.ModelForm):
    user = forms.CharField(disabled=True)
    car = forms.CharField(disabled=True)
    notes = forms.CharField(widget=forms.Textarea(attrs={'size':20}))
    class Meta:
        model = Registration
        fields = ['user', 'car', 'start_time', 'end_time', 'notes']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))
