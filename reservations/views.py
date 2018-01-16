from django.shortcuts import render
from django.http import HttpResponse

from reservations.models import Registration


def show_registrations(request):

    all_registrations = Registration.objects.all().order_by('start_time')
    context = {'all_registrations': all_registrations}
    return render(request, 'reservations/view_registrations.html', context)


def create_registrations(request):
    return HttpResponse('<h3>Create registration</h3>')


def show_subscriptions(request):
    return HttpResponse('<h3>Show subscriptions</h3>')


def profile(request):
    return HttpResponse('<h3>Profile</h3>')
