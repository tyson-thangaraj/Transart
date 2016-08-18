__author__ = 'fanfan, Jiandong Wang'

from django.conf.urls import url

from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [

    url(r'^matchlist/$', views.MatchList.as_view(), name='match_list'),
    url(r'^(?P<pk>[0-9]+)/$', views.MatchDetail.as_view(), name='match news detail'),
    url(r'^feedback/', views.user_feedback, name='user feedback'),
]


urlpatterns = format_suffix_patterns(urlpatterns)