from django import forms

from reservations.models import Registration


class RegistrationCreateForm(forms.ModelForm):
    user = forms.CharField(disabled=True)
    car = forms.CharField(disabled=True)

    class Meta:
        model = Registration
        fields = ['user', 'car', 'start_time', 'end_time', 'notes']