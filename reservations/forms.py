from django import forms
from django.contrib.auth.models import User
from django.forms import SelectDateWidget
from reservations.models import Registration, Car, CarCommentary
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class RegistrationCreateForm(forms.ModelForm):
    user = forms.ModelChoiceField(label=_("User"), queryset=User.objects.all(), disabled=True)
    car = forms.ModelChoiceField(label=_("Car"), queryset=Car.objects.all(), disabled=True)
    notes = forms.CharField(label=_("Notes"), widget=forms.Textarea(attrs={'size': 20}), required=False)
    start_time = forms.DateField(label=_("Start date"), widget=SelectDateWidget, disabled=True)
    end_time = forms.DateField(label=_("End date"), widget=SelectDateWidget, disabled=True)

    class Meta:
        model = Registration
        fields = ['user', 'car', 'start_time', 'end_time', 'notes']


class TechnicalForm(forms.ModelForm):
    comment = forms.CharField(label=_("Comment"), widget=forms.Textarea(attrs={'size': 20}))
    user = forms.ModelChoiceField(label=_("User"), queryset=User.objects.all(), disabled=True)
    car = forms.ModelChoiceField(label=_("Car"), queryset=Car.objects.all(), disabled=True)
    date = forms.DateField(label=_("Date"), widget=SelectDateWidget, disabled=True)
    photo = forms.FileField(label=_("Photo"), required=False)

    class Meta:
        model = CarCommentary
        fields = ['user', 'car', 'date', 'comment', 'photo']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label=_("Username"), max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label=_("Password"), max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))


class RegistrationUpdateForm(forms.ModelForm):
    user = forms.ModelChoiceField(label=_("User"), queryset=User.objects.all(), disabled=True)
    car = forms.ModelChoiceField(label=_("Car"), queryset=Car.objects.all(), disabled=True)
    notes = forms.CharField(label=_("Notes"), widget=forms.Textarea(attrs={'size': 20}), required=False)
    start_time = forms.DateField(label=_("Start date"), widget=SelectDateWidget,disabled=True)
    end_time = forms.DateField(label=_("End date"), widget=SelectDateWidget,disabled=True)

    class Meta:
        model = Registration
        fields = ['user', 'car', 'start_time', 'end_time', 'notes']