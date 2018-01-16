from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Car(models.Model):
    brand = models.CharField(max_length=40, verbose_name="Brand")
    name = models.CharField(max_length=40, verbose_name="Name")
    reg_number = models.CharField(max_length=6, verbose_name="Registration number", unique=True)
    type = models.CharField(max_length=40, verbose_name="Type")
    year = models.IntegerField(verbose_name="Release year")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User")
    name = models.CharField(max_length=40, verbose_name="Name")
    surname = models.CharField(max_length=40, verbose_name="Surname")
    phone = models.CharField(max_length=8, verbose_name="Phone", blank=True, null=True)
    email = models.EmailField(verbose_name="Email", blank=True, null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Registration(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Car")
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="User")
    start_time = models.DateTimeField(verbose_name="Start time")
    end_time = models.DateTimeField(verbose_name="End time")
    notes = models.CharField(max_length=500, verbose_name="Note")


class CarCommentary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Car")
    comment = models.CharField(max_length=500)
    date = models.DateTimeField(verbose_name="Commentary date")
