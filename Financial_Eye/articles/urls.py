__author__ = 'fanfan'

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.article_index, name='article_index'),

    url(r'^article_list/$', views.article_list, name='article_list'),
    url(r'^(?P<article_id>[0-9]+)/$', views.article_detail_id, name='article_detail_id'),
    
    url(r'^article_api_list/$', views.ArticleList.as_view(), name='articles_api_list'),
    url(r'^articles/(?P<pk>[0-9]+)/$', views.ArticleDetail.as_view()),
]


#urlpatterns = format_suffix_patterns(urlpatterns)