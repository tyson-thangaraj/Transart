from django.db import models

from articles.models import Article

# Create model: Articlematch
class Articlematch(models.Model):
    News = models.ForeignKey(Article, on_delete=models.CASCADE)  #BBC news, Based news.
    Match_News= models.IntegerField()   # ID of news which matched with bbc news
    Weight = models.FloatField(max_length = 100)   #weight of mixture similarity
    Content_similarity = models.FloatField(max_length = 100, null=True)  #cosine similarity of content similarity
    Name_similarity = models.FloatField(max_length = 100, null=True)  #name entities similarity
    User_feedback = models.FloatField(max_length = 100, default=0)    #sum of user feedback
    class Meta:
        unique_together = (("News", "Match_News"),)    #unique