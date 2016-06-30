
from django.shortcuts import render

# Create your views here.

import urllib
import json
import copy

from django.http import HttpResponse

#from django.shortcuts import render, get_object_or_404
from django.utils.timezone import utc
from datetime import timedelta, datetime
#from rest_framework.decorators import api_view
#from rest_framework import status
from rest_framework.response import Response

from articles.models import Article
from articles.serializers import ArticleSerializer
from rest_framework import generics
from rest_framework import filters
import django_filters

class ArticleFilter(filters.FilterSet):
    latestDatetime = django_filters.IsoDateTimeFilter(name="DateTime", lookup_expr='gt')
    Source = django_filters.CharFilter(lookup_expr='iexact')
    class Meta:
        model = Article
        fields = ['latestDatetime']

class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (filters.OrderingFilter,filters.DjangoFilterBackend,)
    filter_class = ArticleFilter
    #filter_fields = ('Source',)
    ordering_fields  = ('DateTime',)
    ordering = ('-DateTime',)
    
    # def get_queryset(self):
    #     queryset = Article.objects.all()
    #     datetime = self.request.query_params.get('datetime', None)
    #     if datetime is not None:
    #         queryset = queryset.filter(DateTime__gt=datetime)
    #     return queryset


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer




def article_index(request):
    return HttpResponse("Hello, world. You're at the articles index view.")


def article_detail_id(request, article_id):
    article = Article.objects.filter(pk=article_id).first()
    if not article:
        return render(request, 'article_detail.html', {'error_message': "Article reading error."})

    else:
        return render(request, 'article_detail.html',
                      {'article': article})


def article_list(request):
    try:

        th = datetime.now().replace(tzinfo=utc) - timedelta(hours=24)
        #list_of_articles = Article.objects.filter(DateTime__gte=th).order_by('-DateTime')
        list_of_articles = Article.objects.filter().order_by('-DateTime')

        return render(request, 'article_list.html',
                      {'latest_articles_list': list_of_articles, 'total': len(list_of_articles)})
    except:
        return render(request, 'article_list.html')



# @api_view(['GET', 'POST'])
# def article_api_list(request, format=None):
#     """
#     List all articles, or create a new Article.
#     """
#     if request.method == 'GET':
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def article_detail(request, pk, format=None):
#     """
#     Retrieve, update or delete a article instance.
#     """
#     try:
#         article = Article.objects.get(pk=pk)
#     except Article.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = ArticleSerializer(article, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
