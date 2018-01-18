from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, UpdateView, CreateView, ListView
from aurent import settings
from reservations.models import Registration, Car, Profile, Subscription
from .forms import RegistrationCreateForm, RegistrationUpdateForm
from reservations.models import Registration, Car, Profile, CarCommentary
from .forms import RegistrationCreateForm, TechnicalForm
import datetime, json, pytz
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.utils import timezone
utc = pytz.UTC


@login_required(login_url='login')
def show_registrations(request):
    all_registrations = Registration.objects.filter(user=request.user).filter(end_time__gte=timezone.now()).order_by(
        'start_time')
    context = {'all_registrations': all_registrations}

    return render(request, 'reservations/view_registrations.html', context)


@login_required(login_url='login')
def show_subscriptions(request):
    user_subs = Subscription.objects.filter(user=request.user)

    subscribed_cars = []
    for sub in user_subs:
        subscribed_cars.append(sub.car)

    all_cars = Car.objects.all().order_by('name')
    free_cars = []
    for car in all_cars:
        if car not in subscribed_cars:
            free_cars.append(car)

    return render(request, 'reservations/subscriptions_view.html',
                  {'free_cars': free_cars, 'subscribed_cars': subscribed_cars})


@login_required(login_url='login')
def create_subscription(request, car):
    if Subscription.objects.filter(user_id=request.user.id, car_id=car).count() > 0:
        raise Http404()
    sub = Subscription.objects.create(user_id=request.user.id, car_id=car)
    sub.save()
    return redirect(reverse_lazy('reservations:subscriptions'))


@login_required(login_url='login')
def delete_subscription(request, car):
    subs = Subscription.objects.filter(user_id=request.user.id, car_id=car)
    if (subs.count() > 0):
        subs.delete()
    return redirect(reverse_lazy('reservations:subscriptions'))


@login_required(login_url='login')
def profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    return render(request, 'reservations/profile.html', {'user': user, 'profile': profile})


def car_view(request):
    data = Car.objects.all().order_by('name')
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
    template_name = 'reservations/create_registration_form.html'
    success_url = reverse_lazy('reservations:view-registrations')
    form_class = RegistrationCreateForm

    def get_initial(self):
        end_date = utc.localize(datetime.datetime.strptime(self.kwargs['end_date'], "%d-%m-%Y"))
        start_date = utc.localize(datetime.datetime.strptime(self.kwargs['start_date'], "%d-%m-%Y"))
        return {'car': self.kwargs['car'], 'user': self.request.user.pk, 'start_time': start_date, 'end_time': end_date}

    def form_valid(self, form):
        self.object = form.save()
        all_subs = Subscription.objects.all()
        car = Car.objects.get(pk=self.kwargs['car'])
        subbed_users = []
        for sub in all_subs:
            if car == sub.car:
                subbed_users.append(sub.user)
        subbed_emails = []
        for usr in subbed_users:
            subbed_emails.append(Profile.objects.get(user=usr).email)

        send_mail(
            'Aurent automatic subscribtion message',
            'Car: ' + car.__str__() + ' was reserved from ' + self.kwargs['start_date'] + ' to ' + self.kwargs['end_date'],
            settings.EMAIL_HOST_USER,
            subbed_emails,
            fail_silently=True,
        )
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required(login_url='login'), name='dispatch')
class RegistrationDelete(DeleteView):
    model = Registration
    success_url = reverse_lazy('reservations:view-registrations')


@method_decorator(login_required(login_url='login'), name='dispatch')
class RegistrationUpdate(UpdateView):
    template_name = 'reservations/create_registration_form.html'
    model = Registration
    form_class = RegistrationUpdateForm
    success_url = reverse_lazy('reservations:view-registrations')


@method_decorator(login_required(login_url='login'), name='dispatch')
class TechnicalUpdate(CreateView):
    model = CarCommentary
    form_class = TechnicalForm
    template_name = 'reservations/create_car_commentary_form.html'
    success_url = reverse_lazy('reservations:view-registrations')

    def get_initial(self):
        return {'user': self.request.user.pk, 'car': self.kwargs['car'], 'date': timezone.now()}
