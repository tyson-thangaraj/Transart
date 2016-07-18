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

    # extract the keywords
    extractKeywords(a1, vectorizer, ID)

    articles_similarity(a1,ID)


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


# fetch the keywords based on the values of TF-IDF
def extractKeywords(newsarray, vectorizer, ids):
    total_features = set()
    i = 0  # get the corresponding id of the news
    for item in newsarray:
        # sort the value of tf-idf
        indices = np.argsort(item)[::-1]
        features = vectorizer.get_feature_names()
        # get top_n features
        top_n = 20
        top_features = [features[i] for i in indices[:top_n]]
        news_id = ids[i]

        # save the keywords to the article object based on the pk
        article = Article.objects.get(pk=news_id)
        article.Keywords = str(top_features)
        article.save()
        i = i+1
        in_feature = set(top_features)
        total_features = total_features | in_feature


# save the matched news to database
def articles_similarity(newsarray,ids):
    pk1 = 0
    for item1 in newsarray:
        pk2 = 0

        article = Article.objects.get(pk=ids[pk1])
        if(article.Source != "BBC"):
            pk1 = pk1+1
            continue
        for item2 in newsarray:
            # article2 = Article.objects.get(pk=ids[pk2])
            # if(article2.Source == "BBC"):
            #     pk2 = pk2+1
            #     continue
            if pk1 != pk2:
                try:
                    get_object_or_404(Articlematch, News=article, Match_News = ids[pk2])
                except:
                    try:
                        #get the cosine score of this two articles based on the tf-idf
                        simi = cosine_similarity(item1, item2)
                        # save
                        articlematch = Articlematch(News = article, Match_News=ids[pk2], Weight = simi)
                        articlematch.save()
                    except Exception as err:
                        print(err)
                        print("Failed adding matched article ")
                        pass
                    else:
                        #print("Add New matched Article:" + articlematch.News.id + articlematch.Match_News + articlematch.Weight)
                        print("Add New matched Article  +++++++++++++++++++++++++++++++++++++++++++++++")
            pk2 = pk2+1
        pk1 = pk1+1