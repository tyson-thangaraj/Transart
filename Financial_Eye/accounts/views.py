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

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

# class ArticleFilter(filters.FilterSet):
#     latestDatetime = django_filters.IsoDateTimeFilter(name="DateTime", lookup_expr='gt')
#     Source = django_filters.CharFilter(lookup_expr='iexact')
#     class Meta:
#         model = Article
#         fields = ['latestDatetime']
#
# class ArticleList(generics.ListCreateAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     filter_backends = (filters.OrderingFilter,filters.DjangoFilterBackend,)
#     filter_class = ArticleFilter
#     #filter_fields = ('Source',)
#     ordering_fields  = ('DateTime',)
#     ordering = ('-DateTime',)
#
#     # def get_queryset(self):
#     #     queryset = Article.objects.all()
#     #     datetime = self.request.query_params.get('datetime', None)
#     #     if datetime is not None:
#     #         queryset = queryset.filter(DateTime__gt=datetime)
#     #     return queryset
