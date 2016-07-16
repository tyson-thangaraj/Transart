__author__ = 'fanfan'
#


import json
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

from articles.models import Article
from django.core import serializers
from articles.serializers import ArticleSerializer

def matcharticlesbydate(th):
<<<<<<< Updated upstream
    data = serializers.serialize("json", Article.objects.filter(DateTime__gte = th), fields=('Content'))
=======
    news = serializers.serialize("json", Article.objects.filter(DateTime__gte = th))
    news = json.loads(news)
    contents=[]
    ID=[]
    j=0 #store tha value of the number of documents
    #print(news)
    print(type(news))
    #Extract raw descriptions and the corresponding two class labels for those descriptions
    for item in news:
        contents.append(item["fields"]["Content"])
        ID.append(item["pk"])
        j=j+1
    print(j)
    #turn the corpus content into numerical feature vectors to help make classify
    #TfidfVectorizer is equal to CountVectorizer followed by TfidfTransformer
    vectorizer = TfidfVectorizer(stop_words="english",lowercase=True,min_df = 2,tokenizer=lemma_tokenizer)

    #Learn vocabulary and idf and Transform documents to document-term matrix.
    X = vectorizer.fit_transform(contents)
    print(X.shape)


    #sort the tf-idf and find most important words for each news
    a1=X.toarray()
    total_features = set()

    for item in a1:
        indices = np.argsort(item)[::-1]
        features = vectorizer.get_feature_names()
        top_n = 20
        top_features = [features[i] for i in indices[:top_n]]
        print(top_features)
        in_feature = set(top_features)
        total_features = total_features | in_feature
    print(total_features)

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

>>>>>>> Stashed changes
