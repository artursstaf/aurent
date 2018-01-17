from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView, CreateView, ListView
from reservations.models import Registration, Car
from .forms import RegistrationCreateForm
import datetime, json
import pytz

utc = pytz.UTC

def show_registrations(request):
    all_registrations = Registration.objects.all().order_by('start_time')
    context = {'all_registrations': all_registrations}
    return render(request, 'reservations/view_registrations.html', context)


def show_subscriptions(request):
    return HttpResponse('<h3>Show subscriptions</h3>')


def profile(request):
    return HttpResponse('<h3>Profile</h3>')


def car_view(request):
    data = Car.objects.all()
    available_cars = []
    registrations = Registration.objects.all()
    start_date = utc.localize(datetime.datetime.strptime(request.GET.get('start_date'), "%d-%m-%Y"))
    end_date = utc.localize(datetime.datetime.strptime(request.GET.get('end_date'), "%d-%m-%Y"))
    not_available_cars = []
    for reg in registrations:
        if ((reg.start_time >= start_date and reg.start_time <= end_date)
            or (reg.end_time >= start_date and reg.end_time <= end_date)
            or (reg.start_time <= start_date and reg.end_time >= end_date)):
            not_available_cars.append(reg.car_id)
    for car in data:
        if car.id not in not_available_cars:
            available_cars.append(car.as_json())
    car_list = list(available_cars)
    return JsonResponse(json.dumps(car_list), safe=False)


class CarsList(ListView):
    model = Car
    template_name = 'reservations/view_cars.html'


class RegistrationCreate(CreateView):
    model = Registration
    template_name = 'reservations/update_add_form_group.html'
    success_url = reverse_lazy('reservations:view-registrations')
    form_class = RegistrationCreateForm

    def get_initial(self):
        return {'car': Car.objects.all(), 'user': self.request.user}

class RegistrationDelete(DeleteView):
    model = Registration
    success_url = reverse_lazy('reservations:view-registrations')


class RegistrationUpdate(UpdateView):
    template_name = 'reservations/update_add_form_group.html'
    model = Registration
    fields = ['user', 'car', 'start_time', 'end_time', 'notes']
    success_url = reverse_lazy('reservations:view-registrations')
