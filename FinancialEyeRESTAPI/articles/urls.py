from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from articles import views

urlpatterns = [
    url(r'^articles/$', views.article_list),
    url(r'^articles/(?P<pk>[0-9]+)/$', views.article_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)