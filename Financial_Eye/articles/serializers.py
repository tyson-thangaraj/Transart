__author__ = 'fanfan'

from rest_framework import serializers
# from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from articles.models import  Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('Headline', 'SubHeadline', 'Url', 'DateTime', 'Keywords', 'Content', 'Type', 'Source')


