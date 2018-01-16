from django.urls import re_path
from . import views

app_name = 'reservations'

urlpatterns = [
    re_path(r'^$', views.show_registrations, name='view-registrations'),
    re_path(r'^subscriptions$', views.show_subscriptions, name='subscriptions'),
    re_path(r'^profile', views.profile, name='profile'),
    re_path(r'^cars', views.CarsList.as_view(), name='all-cars'),


    re_path(r'^create/(?P<car>[0-9]+)$', views.RegistrationCreate.as_view(), name='create-registrations'),
    re_path(r'^registration/(?P<pk>[0-9]+)/delete$', views.RegistrationDelete.as_view(), name='delete-registration'),
    re_path(r'^registration/(?P<pk>[0-9]+)/update$', views.RegistrationUpdate.as_view(), name='update-registration'),
]
