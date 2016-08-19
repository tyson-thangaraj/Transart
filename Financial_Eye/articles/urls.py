__author__ = 'fanfan, Jiandong Wang'

from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^article_api_list/$', views.ArticleList.as_view(), name='articles_api_list'),
    url(r'^articles/(?P<pk>[0-9]+)/$', views.ArticleDetail.as_view()),
]


#urlpatterns = format_suffix_patterns(urlpatterns)