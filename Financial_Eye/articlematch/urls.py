__author__ = 'fanfan'

from django.conf.urls import url

from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [

    url(r'^matchlist/$', views.MatchList.as_view(), name='match_list'),
    url(r'^(?P<pk>[0-9]+)/$', views.MatchDetail.as_view(), name='match news detail'),
]


urlpatterns = format_suffix_patterns(urlpatterns)