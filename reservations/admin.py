from django.contrib import admin
from .models import Car, Profile, Registration, CarCommentary, Subscription

# Register your models here.
admin.site.register(Car)
admin.site.register(Profile)
admin.site.register(Registration)
admin.site.register(CarCommentary)
admin.site.register(Subscription)
