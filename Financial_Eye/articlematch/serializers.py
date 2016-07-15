__author__ = 'fanfan'

from rest_framework import serializers
# from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from articlematch.models import Articlematch
from articles.models import  Article

class ArticlematchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articlematch
        fields = ('Match_News', 'News', 'Weight')
