from django.shortcuts import render


from django.http import HttpResponse

#from django.shortcuts import render, get_object_or_404
from django.utils.timezone import utc
# from datetime import timedelta, datetime
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from accounts.models import Users
from accounts.serializers import UserSerializer
from rest_framework import generics
from rest_framework import filters
import django_filters

# Create your views here.

@api_view(['GET', 'POST'])
def UserList(request, format=None):
    """
    List all articles, or create a new Article.
    """
    if request.method == 'GET':
        users = Users.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def UserDetail(request, pk, format=None):
    """
    Retrieve, update or delete a article instance.
    """
    try:
        users = Users.objects.get(pk=pk)
    except Users.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(users)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(users, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        users.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
