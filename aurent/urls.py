"""aurent URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, re_path
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth.views import login
from django.contrib.auth.views import logout
from reservations.forms import LoginForm
from reservations.views import change_password

urlpatterns = []
urlpatterns += i18n_patterns(
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^registrations/', include('reservations.urls')),
    re_path(r'^logout/$', logout, {'next_page': 'login'}, name='logout'),
    re_path(r'^login/$', login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
    re_path(r'^password/$', change_password, name='change_password'),
)
