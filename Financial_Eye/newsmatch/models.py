from django.db import models

# Create your models here.
from articles.models import Article

class Newsmatch(models.Model):
    News = models.ForeignKey(Article, on_delete=models.CASCADE)
    Match_News= models.IntegerField()
    Weight = models.FloatField(max_length = 100)
    class Meta:
        unique_together = (("News", "Match_News"),)