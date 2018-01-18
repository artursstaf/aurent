from django.urls import re_path, path

from reservations.forms import LoginForm
from . import views

app_name = 'reservations'


urlpatterns = [
    re_path(r'^$', views.show_registrations, name='view-registrations'),
    re_path(r'^subscriptions$', views.show_subscriptions, name='subscriptions'),
    re_path(r'^subscriptions/create/(?P<car>[0-9]+)$', views.create_subscription, name='create-subscriptions'),
    re_path(r'^subscriptions/delete/(?P<car>[0-9]+)$', views.delete_subscription, name='delete-subscriptions'),
    re_path(r'^comments/(?P<car>[0-9]+)$', views.view_comments, name='view-comments'),
    re_path(r'^profile', views.profile, name='profile'),
    re_path(r'^cars', views.CarsList.as_view(), name='all-cars'),
    re_path(r'^test$', views.car_view, name='test-cars'),
    re_path(r'^create/(?P<car>[0-9]+)/(?P<start_date>\d{2}-\d{2}-\d{4})/(?P<end_date>\d{2}-\d{2}-\d{4})$', views.RegistrationCreate.as_view(), name='create-registrations'),
    re_path(r'^registration/(?P<pk>[0-9]+)/delete$', views.RegistrationDelete.as_view(), name='delete-registration'),
    re_path(r'^registration/(?P<pk>[0-9]+)/update$', views.RegistrationUpdate.as_view(), name='update-registration'),
    re_path(r'^technical_update/(?P<car>[0-9]+)$', views.TechnicalUpdate.as_view(), name='technical-update'),
]
