from django.db import models

# Create your models here.

class Users(models.Model):
    Username = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    Email = models.EmailField(blank=True)
    FirstName = models.CharField(max_length=50, blank=True)
    LastName = models.CharField(max_length=50, blank=True)
    Address = models.CharField(max_length=500, blank=True)
    Telephone = models.CharField(max_length=20, blank=True)
    DateJoined = models.DateTimeField('RegisterDate', blank=True)