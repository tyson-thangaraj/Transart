from django.shortcuts import render


from django.http import HttpResponse

#from django.shortcuts import render, get_object_or_404
from django.utils.timezone import utc
# from datetime import timedelta, datetime
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from accounts.models import Users
from accounts.serializers import UserSerializer
from rest_framework import generics
from rest_framework import filters
import django_filters

# Create your views here.

class UserList(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Users.objects.all()
        username = self.request.query_params.get('username', None)
        password = self.request.query_params.get('password', None)
        flag = self.request.query_params.get('flag', None)
        # print(flag)
        # print(type(flag))
        if flag == "1":
            newuser = Users(Username=username, Password=password)
            newuser.save()
        elif flag == "2":
            if username and password is not None:
                queryset = queryset.filter(Username=username, Password=password)
            return queryset

class CreateUser(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    def get_queryset(self):
        queryset = Users.objects.all()
        print("hello")
        username = self.request.query_params.get('username', None)
        password = self.request.query_params.get('password', None)
        newuser = Users(Username=username, Password=password)
        if newuser.save():
            print("created success!")
            queryset = queryset.filter(Username=username, Password=password)
            return queryset

        # if username and password is not None:
        #     queryset = queryset.filter(Username=username, Password=password)
        # return queryset


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

def createUserObject(username, password, email,firstname, lastname, address, telephone, datejoined):
    print([username, password, email,firstname, lastname, address, telephone, datejoined])
    try:
        user = Users(Username=username,
                        Password=password,
                        Email=email,
                        FirstName = firstname,
                        LastName = lastname,
                        Address = address,
                        Telephone = telephone,
                        DateJoined = datejoined)

    except Exception as err:
                print("In createArticleObject():"+ err)
    return user