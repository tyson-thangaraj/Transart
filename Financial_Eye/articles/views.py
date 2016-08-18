
__author__ = 'Jiandong Wang'
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.timezone import utc
from datetime import timedelta, datetime
from articles.models import Article
from articles.serializers import ArticleSerializer
from rest_framework import generics
from rest_framework import filters
import django_filters




# customize the filter
class ArticleFilter(filters.FilterSet):
    latestDatetime = django_filters.IsoDateTimeFilter(name="DateTime", lookup_expr='gt')
    #Source_for_web_use =ChoiceFilter( choices=Article.objects.values_list('Source',flat=True).distinct())
    Source = django_filters.CharFilter(lookup_expr='iexact')
    class Meta:
        model = Article
        fields = ['latestDatetime']

class ArticleList(generics.ListCreateAPIView):
    # only display news published in 5 days
    th = datetime.now().replace(tzinfo=utc) - timedelta(hours=24*5)
    queryset = Article.objects.filter(DateTime__gte = th).order_by('-DateTime')
    serializer_class = ArticleSerializer
    #set filter, ordering
    filter_backends = (filters.OrderingFilter,filters.DjangoFilterBackend,)
    filter_class = ArticleFilter
    ordering_fields  = ('DateTime',)
    ordering = ('-DateTime',)
    
class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


# def article_index(request):
#     return HttpResponse("Hello, world. You're at the articles index view.")


# def article_detail_id(request, article_id):
#     article = Article.objects.filter(pk=article_id).first()
#     if not article:
#         return render(request, 'article_detail.html', {'error_message': "Article reading error."})

#     else:
#         return render(request, 'article_detail.html',
#                       {'article': article})


# def article_list(request):
#     try:

#         # th = datetime.now().replace(tzinfo=utc) - timedelta(hours=24*500)
#         # print('-------------------------------------')
#         # print(th)
#         # list_of_articles = Article.objects.filter(DateTime__gte = th).order_by('-DateTime')
#         list_of_articles = Article.objects.filter().order_by('-DateTime')

#         return render(request, 'article_list.html',
#                       {'latest_articles_list': list_of_articles, 'total': len(list_of_articles)})
#     except:
#         return render(request, 'article_list.html')
