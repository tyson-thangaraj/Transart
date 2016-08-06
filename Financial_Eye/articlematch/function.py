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
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

def matcharticlesbydate(th):

    news = serializers.serialize("json", Article.objects.filter(DateTime__gte = th))
    news = json.loads(news)
    # bbc_news = serializers.serialize("json", Article.objects.filter(DateTime__gte = th, Source = "BBC"))
    # print(news)

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
    tokens_arrays=X.toarray()

    # extract the keywords
    extractKeywords(tokens_arrays, vectorizer, ID)

    articles_similarity(contents,tokens_arrays,ID)


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
def articles_similarity(contents,newsarray,ids):
    pk1 = 0
    for item1 in newsarray:
        pk2 = 0
        article = Article.objects.get(pk=ids[pk1])
        # fetch the name entity
        name1 = extract_entities(contents[pk1])
        entities1=split_name(name1)

        if(article.Source != "BBC"):
            pk1 = pk1+1
            continue
        for item2 in newsarray:
            if pk1 != pk2:
                try:
                    get_object_or_404(Articlematch, News=article, Match_News = ids[pk2])
                except:
                    try:
                        #get the cosine score of this two articles based on the tf-idf
                        contents_similarity = cosine_similarity(item1, item2)
                        # print(contents_similarity)
                        name2 = extract_entities(contents[pk2])
                        entities2=split_name(name2)

                        result= set(entities1+entities2)

                        d1=get_all_word_counts(result,entities1)
                        d2=get_all_word_counts(result,entities2)
                        names_similarity = cosine_similarity(list(d1.values()),list(d2.values()))
                        
                        if names_similarity == 0:
                            simi = 0.8 * contents_similarity
                        else:
                            simi = (0.5 * names_similarity + contents_similarity) * 0.8
                        # save
                        articlematch = Articlematch(News = article, Match_News=ids[pk2], Weight = simi, Content_similarity = contents_similarity, Name_similarity = names_similarity)
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


# Name entities
def extract_entities(text):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    prev = None
    continuous_chunk = []
    current_chunk = []

    for i in chunked:
        if type(i) == Tree:
            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue

    return continuous_chunk

#find name entity from certain text
# def find_name(st, text):
#     name_set = []
#     for sent in nltk.sent_tokenize(text):
#         tokens = nltk.tokenize.word_tokenize(sent)
#         tags = st.tag(tokens)
#         for tag in tags:
#             if tag[1]=='PERSON': name_set.append(tag[0])
#         return name_set

#count each name frequence
def get_all_word_counts(wordunion,entities):
    word_counts=dict((el,0) for el in wordunion)
    for word in entities:
        if word in word_counts:     #If not already there
            word_counts[word]+=1          #Increment the count accordingly
    return word_counts

def split_name(namelist):
    new_name=[]
    for element in namelist:
        parts=element.split( )
        new_name.append(parts)
    # collect both full names and split names
    results_union = set().union(*new_name, namelist)
    name_union=list(results_union)
    return name_union