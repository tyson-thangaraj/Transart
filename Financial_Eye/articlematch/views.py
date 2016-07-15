from django.shortcuts import render

# Create your views here.

from articlematch.models import Articlematch
from articlematch.serializers import ArticlematchSerializer
from rest_framework import generics

class MatchList(generics.ListCreateAPIView):
    queryset = Articlematch.objects.all()
    serializer_class = ArticlematchSerializer


class MatchDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Articlematch.objects.all()
    serializer_class = ArticlematchSerializer