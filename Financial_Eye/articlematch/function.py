__author__ = 'fanfan'
#

from articles.models import Article
from django.core import serializers
from articles.serializers import ArticleSerializer

def matcharticlesbydate(th):
    data = serializers.serialize("json", Article.objects.filter(DateTime__gte = th), fields=('Content'))