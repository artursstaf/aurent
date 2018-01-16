from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView, CreateView, ListView

from reservations.models import Registration, Car
from .forms import RegistrationCreateForm

def show_registrations(request):

    all_registrations = Registration.objects.all().order_by('start_time')
    context = {'all_registrations': all_registrations}
    return render(request, 'reservations/view_registrations.html', context)


def show_subscriptions(request):
    return HttpResponse('<h3>Show subscriptions</h3>')


def profile(request):
    return HttpResponse('<h3>Profile</h3>')


class CarsList(ListView):
    model = Car
    template_name = 'reservations/view_cars.html'


class RegistrationCreate(CreateView):
    model = Registration
    template_name = 'reservations/update_add_form_group.html'
    success_url = reverse_lazy('reservations:view-registrations')
    form_class = RegistrationCreateForm

    def get_initial(self):
        return {'car': self.kwargs['car'], 'user': 0}

class RegistrationDelete(DeleteView):
    model = Registration
    success_url = reverse_lazy('reservations:view-registrations')


class RegistrationUpdate(UpdateView):
    template_name = 'reservations/update_add_form_group.html'
    model = Registration
    fields = ['user', 'car', 'start_time', 'end_time', 'notes']
    success_url = reverse_lazy('reservations:view-registrations')
