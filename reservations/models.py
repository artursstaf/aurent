from django.db import models


class Car(models.Model):
    brand = models.CharField(max_length=40, verbose_name="Brand")
    name = models.CharField(max_length=40, verbose_name="Name")
    reg_number = models.CharField(max_length=6, verbose_name="Registration number", unique=True)
    type = models.CharField(max_length=40, verbose_name="Type")
    year = models.IntegerField(verbose_name="Release year")


class User(models.Model):
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    role = models.CharField(max_length=40, default="employee")


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