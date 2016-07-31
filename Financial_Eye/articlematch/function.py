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
from nltk.tag.stanford import StanfordNERTagger

def matcharticlesbydate(th):

    news = serializers.serialize("json", Article.objects.filter(DateTime__gte = th))
    news = json.loads(news)
    bbc_news = serializers.serialize("json", Article.objects.filter(DateTime__gte = th, Source = "BBC"))
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

    #name entities
    name_entities = extract_name_entity(contents)
    print(name_entities)
    # extract the keywords
    extractKeywords(tokens_arrays, vectorizer, ID)

    articles_similarity(contents,tokens_arrays,ID, name_entities)


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
def articles_similarity(contents,newsarray,ids, names):
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
                        contents_similarity = cosine_similarity(item1, item2)
                        # print(contents_similarity)
                        names_similarity = name_entity_similarity(names,contents, pk1, pk2)
                        # print(names[pk1])
                        # print(names[pk2])
                        # print(names_similarity)
                        simi = 0.6 * names_similarity + 0.4 * contents_similarity
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
def extract_name_entity(contents):

    # First we set the direct path to the NER Tagger.
    _model_filename = r'/Users/fanfan/Documents/ucd/S3/01_project/Transart/Temporary Code/ExtractNames/stanford-ner/stanford-ner-2015-04-20/classifiers/english.all.3class.distsim.crf.ser.gz'
    _path_to_jar = r'/Users/fanfan/Documents/ucd/S3/01_project/Transart/Temporary Code/ExtractNames/stanford-ner/stanford-ner-2015-04-20/stanford-ner.jar'
    # Then we initialize the NLTK's Stanford NER Tagger API with the DIRECT PATH to the model and .jar file.
    st = StanfordNERTagger(model_filename=_model_filename, path_to_jar=_path_to_jar)
    # i = 0
    name_contents = []

    for item in contents:
        #print(find_name(st,item))
        name_contents.append((find_name(st,item)))
    #     i = i+1
    # print(i)
    return name_contents

#find name entity from certain text
def find_name(st, text):
    name_set = []
    for sent in nltk.sent_tokenize(text):
        tokens = nltk.tokenize.word_tokenize(sent)
        tags = st.tag(tokens)
        for tag in tags:
            if tag[1]=='PERSON': name_set.append(tag[0])
        return name_set

#merge two name sets
def union(a,b):
    for e in b:
        if e not in a:
            a.append(e)
    return a

#count each name frequence
def get_all_word_counts(wordunion,content):
    tokens = nltk.word_tokenize(content)
    words=[]
    for w in tokens:
        words.append(w)

    word_counts=dict((el,0) for el in wordunion)
    for word in words:
        if word in word_counts:     #If not already there
            word_counts[word]+=1          #Increment the count accordingly
    return word_counts

# calculate the cosine similarity of names entities
def name_entity_similarity(names, contents, pk1, pk2):
    # print("hello")
    name_union = union(names[pk1], names[pk2])
    # print(name_union)
    d1=get_all_word_counts(name_union,contents[pk1])
    d2=get_all_word_counts(name_union,contents[pk2])
    # print(d1)
    # print(d2)
    name_similarity = cosine_similarity(list(d1.values()),list(d2.values()))
    # print(name_similarity)
    return name_similarity

