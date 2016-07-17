from django.db import models

# Create your models here.
from articles.models import Article

class Articlematch(models.Model):
    News = models.ForeignKey(Article, on_delete=models.CASCADE)  #BBC news, Based news.
    Match_News= models.IntegerField()   # ID of news which matched with bbc news
    # News = models.IntegerField()  #BBC news, Based news.
    # Match_News= models.ForeignKey(Article, on_delete=models.CASCADE)   # News which matched with bbc news
    Weight = models.FloatField(max_length = 100)
    class Meta:
        unique_together = (("News", "Match_News"),)