from django.shortcuts import render

# Create your views here.

from articlematch.models import Articlematch
from articles.models import Article
from articlematch.serializers import ArticlematchSerializer
from rest_framework import generics
from rest_framework import filters
import django_filters
from rest_framework.pagination import LimitOffsetPagination
# user feedback
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

class MatchFilter(filters.FilterSet):
    selectedArticleID = django_filters.ModelChoiceFilter(name='News', queryset=Article.objects.filter(Source='BBC'))
    class Meta:
        model = Articlematch
        fields = ['selectedArticleID']

class TopNArticlePagination(LimitOffsetPagination):
    default_limit = 1000
    


class MatchList(generics.ListCreateAPIView):
    threshold = 0.35
    queryset = Articlematch.objects.filter(Weight__gte=threshold)
    serializer_class = ArticlematchSerializer

    pagination_class = TopNArticlePagination 
    filter_backends = (filters.OrderingFilter,filters.DjangoFilterBackend,)
    filter_class = MatchFilter
    ordering_fields  = ('News','Weight')
    ordering = ('News', '-Weight')


class MatchDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Articlematch.objects.all()
    serializer_class = ArticlematchSerializer

@api_view(['GET', 'POST'])
def user_feedback(request, format=None):
    """
    collect user feedback for article match
    """

    article = request.query_params.get('original', None)
    matched_article = request.query_params.get('matched', None)
    feedback = request.query_params.get('feedback', None)

    if (not article) | (not matched_article) | (not feedback):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        match = Articlematch.objects.get(News=article, Match_News=matched_article)
        
        # pre_number = match.User_feedback
        # pre_weight = 
        match.User_feedback += int(feedback)
        cur_number = match.User_feedback

        if (cur_number>=0)&(cur_number<=20):
            match.Weight += 0.01*int(feedback)

        match.save()

            
        # match.Weight += 0.01*match.User_feedback 
        # match.save()
        return Response(status=status.HTTP_200_OK)  
    except Articlematch.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

