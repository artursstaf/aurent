from django.urls import re_path
from . import views

app_name = 'reservations'

urlpatterns = [
    re_path(r'^$', views.show_registrations, name='view-registrations'),
    re_path(r'^create$', views.create_registrations, name='create-registrations'),
    re_path(r'^subscriptions$', views.show_subscriptions, name='subscriptions'),
    re_path(r'^profile', views.profile, name='profile'),
]