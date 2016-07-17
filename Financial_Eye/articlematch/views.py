from django.shortcuts import render

# Create your views here.

from articlematch.models import Articlematch
from articles.models import Article
from articlematch.serializers import ArticlematchSerializer
from rest_framework import generics
from rest_framework import filters
import django_filters
from rest_framework.pagination import LimitOffsetPagination


class MatchFilter(filters.FilterSet):
    selectedArticleID = django_filters.ModelChoiceFilter(name='News', queryset=Article.objects.all())
    class Meta:
        model = Articlematch
        fields = ['selectedArticleID']

class TopNArticlePagination(LimitOffsetPagination):
    default_limit = 1000
    


class MatchList(generics.ListCreateAPIView):
    queryset = Articlematch.objects.all()
    serializer_class = ArticlematchSerializer
    pagination_class = TopNArticlePagination 
    filter_backends = (filters.OrderingFilter,filters.DjangoFilterBackend,)
    filter_class = MatchFilter
    ordering_fields  = ('News','Weight')
    ordering = ('News', '-Weight')


class MatchDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Articlematch.objects.all()
    serializer_class = ArticlematchSerializer
