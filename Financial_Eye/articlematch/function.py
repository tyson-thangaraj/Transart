__author__ = 'fanfan'
#


import json
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from django.shortcuts import get_object_or_404

from articles.models import Article
from django.core import serializers
from articlematch.models import Articlematch
from articles.serializers import ArticleSerializer

def matcharticlesbydate(th):

    news = serializers.serialize("json", Article.objects.filter(DateTime__gte = th))
    news = json.loads(news)
    bbc_news = serializers.serialize("json", Article.objects.filter(DateTime__gte = th, Source = "BBC"))

    contents=[]
    ID=[]
    j=0 #store tha value of the number of documents

    #Extract raw descriptions and the corresponding two class labels for those descriptions
    for item in news:
        contents.append(item["fields"]["Content"])
        ID.append(item["pk"])
        j=j+1

    #turn the corpus content into numerical feature vectors to help make classify
    #TfidfVectorizer is equal to CountVectorizer followed by TfidfTransformer
    vectorizer = TfidfVectorizer(stop_words="english",lowercase=True,min_df = 2,tokenizer=lemma_tokenizer)

    #Learn vocabulary and idf and Transform documents to document-term matrix.
    X = vectorizer.fit_transform(contents)
    print(X.shape)

    #sort the tf-idf and find most important words for each news
    a1=X.toarray()

    total_features = set()

    i = 0  # get the corresponding id of the news

    for item in a1:
        indices = np.argsort(item)[::-1]
        features = vectorizer.get_feature_names()
        top_n = 20
        top_features = [features[i] for i in indices[:top_n]]
        news_id = ID[i]

        article = Article.objects.get(pk=news_id)
        article.Keywords = str(top_features)
        article.save()
        i = i+1
        #print(top_features)

        in_feature = set(top_features)
        total_features = total_features | in_feature
    total_words = list(total_features)
    print(len(total_features))
    #print(total_words)

    pk1 = 0
    pk2 = 0
    for item in a1:
        for item2 in a1:
            if pk1 == pk2:
                continue
            simi = cosine_similarity(item, item2)

            article = Article.objects.get(pk=news_id)
            try:
                get_object_or_404(Articlematch, News=article, Match_News = ID[pk2])
            except:
                try:
                    articlematch = Articlematch(News = article, Match_News=ID[pk2], Weight = simi)
                    articlematch.save()
                except Exception as err:
                    print(err)
                    print("Failed adding matched article ")
                    pass
                else:
                    #print("Add New matched Article:" + articlematch.News.id + articlematch.Match_News + articlematch.Weight)
                    print("Add New matched Article:" + articlematch.Match_News + articlematch.Weight)
            pk2 = pk2+1
        pk1 = pk1+1


def lemma_tokenizer(text):
    # use the standard scikit-learn tokenizer first to converting strings of descriptions to a list of tokens
    standard_tokenizer = TfidfVectorizer().build_tokenizer()
    tokens = standard_tokenizer(text)
    # then use NLTK to perform lemmatisation on each token
    lemmatizer = nltk.stem.WordNetLemmatizer()
    lemma_tokens = []
    for token in tokens:
        lemma_tokens.append( lemmatizer.lemmatize(token) )
    return lemma_tokens
