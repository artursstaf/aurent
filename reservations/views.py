from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, UpdateView, CreateView, ListView
from reservations.models import Registration, Car, Profile, CarCommentary
from .forms import RegistrationCreateForm
import datetime, json
import pytz
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.utils import timezone
import datetime

utc = pytz.UTC

@login_required(login_url='login')
def show_registrations(request):
    all_registrations = Registration.objects.filter(user=request.user).filter(end_time__gte=timezone.now()).order_by('start_time')
    context = {'all_registrations': all_registrations}

    return render(request, 'reservations/view_registrations.html', context)


@login_required(login_url='login')
def show_subscriptions(request):
    return render(request, 'reservations/subscriptions_view.html', {})


@login_required(login_url='login')
def profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    return render(request, 'reservations/profile.html', {'user': user, 'profile': profile})



def car_view(request):
    data = Car.objects.all()
    available_cars = []
    start_date = utc.localize(datetime.datetime.strptime(request.GET.get('start_date'), "%d-%m-%Y"))
    end_date = utc.localize(datetime.datetime.strptime(request.GET.get('end_date'), "%d-%m-%Y"))
    if end_date < start_date:
        return JsonResponse(json.dumps(list(available_cars)), safe=False)
    registrations = Registration.objects.all()
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


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('logout')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'reservations/update_add_form_group.html', {
        'form': form
    })


@method_decorator(login_required(login_url='login'), name='dispatch')
class CarsList(ListView):
    model = Car
    template_name = 'reservations/view_cars.html'


@method_decorator(login_required(login_url='login'), name='dispatch')
class RegistrationCreate(CreateView):
    model = Registration
    template_name = 'reservations/update_add_form_group.html'
    success_url = reverse_lazy('reservations:view-registrations')
    form_class = RegistrationCreateForm

    def get_initial(self):
        return {'car': self.kwargs['car'], 'user': self.request.user.pk}


@method_decorator(login_required(login_url='login'), name='dispatch')
class RegistrationDelete(DeleteView):
    model = Registration
    success_url = reverse_lazy('reservations:view-registrations')


@method_decorator(login_required(login_url='login'), name='dispatch')
class RegistrationUpdate(UpdateView):
    template_name = 'reservations/update_add_form_group.html'
    model = Registration
    fields = ['user', 'car', 'start_time', 'end_time', 'notes']
    success_url = reverse_lazy('reservations:view-registrations')


@method_decorator(login_required(login_url='login'), name='dispatch')
class TechnicalUpdate(CreateView):
    model = CarCommentary
    fields = ['user', 'car', 'comment', 'date']
    template_name = 'reservations/technical_update.html'
    success_url = reverse_lazy('reservations:view-registrations')
