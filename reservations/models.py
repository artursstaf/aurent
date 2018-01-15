from django.db import models


class Car(models.Model):
    brand = models.CharField(max_length=20)
    name = models.CharField(max_length=10)
    reg_number = models.CharField(max_length=6)
    type = models.CharField(max_length=10)
    year = models.IntegerField(max_length=4)


class User(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    role = models.CharField(max_length=10, default="employee")


class Registration(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField
    end_time = models.DateTimeField
    notes = models.CharField(max_length=500)
