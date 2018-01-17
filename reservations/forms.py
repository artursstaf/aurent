from django import forms
from django.contrib.auth.models import User
from django.forms import SelectDateWidget

from reservations.models import Registration, Car
from django.contrib.auth.forms import AuthenticationForm

class RegistrationCreateForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), disabled=True)
    car = forms.ModelChoiceField(queryset=Car.objects.all(), disabled=True)
    notes = forms.CharField(widget=forms.Textarea(attrs={'size': 20}))
    start_time = forms.DateField(widget=SelectDateWidget)
    end_time = forms.DateField(widget=SelectDateWidget)

    class Meta:
        model = Registration
        fields = ['user', 'car', 'start_time', 'end_time', 'notes']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))
