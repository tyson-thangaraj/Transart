from django.db import models

# Create model Users: Username, password, Email,FirstName, LastName, Address, Telephone, DateJoined.
class Users(models.Model):
    Username = models.CharField(max_length=50, primary_key=True)
    Password = models.CharField(max_length=50)
    Email = models.EmailField(blank=True, null=True)
    FirstName = models.CharField(max_length=50, blank=True, null=True)
    LastName = models.CharField(max_length=50, blank=True, null=True)
    Address = models.CharField(max_length=500, blank=True, null=True)
    Telephone = models.CharField(max_length=20, blank=True, null=True)
    DateJoined = models.DateTimeField('RegisterDate', blank=True, null=True)