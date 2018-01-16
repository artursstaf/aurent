from django.urls import re_path
from . import views

app_name = 'reservations'

urlpatterns = [
    re_path(r'^$', views.show_registrations, name='view-registrations'),
    re_path(r'^subscriptions$', views.show_subscriptions, name='subscriptions'),
    re_path(r'^profile', views.profile, name='profile'),



    re_path(r'^create$', views.create_registrations, name='create-registrations'),
    re_path(r'^registration/(?P<pk>[0-9]+)/delete$', views.delete_registration, name='delete-registration'),
    re_path(r'^registration/(?P<pk>[0-9]+)/update$', views.update_registration, name='update-registration'),

]
