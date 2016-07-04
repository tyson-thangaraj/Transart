__author__ = 'fanfan'

import urllib
from datetime import datetime
from bs4 import BeautifulSoup
import nltk
import pytz

from articles.models import Article
import newspaper
from http.cookiejar import CookieJar

def createArticleObject(title, subtitle, body, date, keywords, url, type, source, image):
    #print([title, subtitle, body, date, keywords, url, type, source, image])

    try:
        article = Article(Headline=title, SubHeadline=subtitle,
                      Content=body, Url=url,
                      DateTime=date, Keywords=keywords,
                      Type=type,
                      Source=source,
                      Image=image)

    except Exception as err:
                print("In createArticleObject():"+ err)
    return article

def createArticleByUrl(url):
    [title, subtitle, body, date, keywords, source, image] = getArticleDetailsByUrl(url)
    article = createArticleObject(title, subtitle, body, date, keywords, url, "RSS", source, image)
    return article

def getArticleDetailsByUrl(url):
    #print(url)
    article = newspaper.Article(url)
    article.download()
    article.parse()


    title = article.title
    sub_title=article.meta_description
    authors = article.authors
    date = article.publish_date

    news_content = article.text
    image = article.top_image

    article.nlp()
    keywords = article.keywords

    source = "other"
    if "chinadaily" in url:
        source = "ChinaDaily"
    elif "bbc" in url:
        page = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(page,"html.parser")
        soup.prettify()
        source = "BBC"
        tag = soup.find("div", attrs={"class": "date date--v2"})
        date = tag.get_text()
        if "GMT" in date:
            date = datetime.strptime(date, "%d %B %Y")
        else:
            date = datetime.strptime(date, "%d %B %Y")
            local_dt = pytz.timezone('Europe/Dublin').localize(date, is_dst=None)
            date = local_dt.astimezone(pytz.utc)
    elif "nytimes" in url:
        source="The New York Times"
        cj = CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        p = opener.open(url).read()
        soup = BeautifulSoup(p,"html.parser")
        soup.prettify()
        tag = soup.find("meta", attrs={"name": "ptime"}).get('content')
        date = datetime.strptime(tag, "%Y%m%d%H%M%S")
    elif "reuters" in url:
        source="Reuters"
    elif "people" in url:
        source = "People"
        title = str.split(title, '--')[0]
        page = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(page,"html.parser")
        soup.prettify()
        news_content=''
        for tag in soup.find("div", attrs={"class": "box_con"}).find_all("p"):
            if "script" not in tag.get_text():
                news_content += tag.get_text() + '\n'
        keywords = extractKeywords(title)
    elif "sina" in url:
        page = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(page,"html.parser")
        soup.prettify()
        source = "Sina"
        news_content=''
        for tag in soup.find("div", attrs={"id": "artibody"}).find_all("p"):
            if "JavaScript" not in tag.get_text():
                news_content += tag.get_text() + '\n'
        keywords = extractKeywords(title)

    return [title, sub_title, news_content, date, keywords, source, image]

def extractKeywords(text):
    stop_words = load_stopwords()
    keywords = []
    tokens = nltk.word_tokenize(text)
    #print(tokens)

    for token in tokens:
        if token not in stop_words:
            keywords.append(token.lower())

    #print(keywords)
    return ", ".join(keywords)

def load_stopwords():
    stop_words = nltk.corpus.stopwords.words('english')
    # custom stop words
    stop_words.extend(['this', 'that', 'the', 'might', 'have', 'been', 'from',
                           'but', 'they', 'will', 'has', 'having', 'had', 'how', 'went'
                            'were', 'why', 'and', 'still', 'his','her',
                           'was', 'its', 'per', 'cent',
                           'a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am', 'among',
                           'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'but', 'by', 'can',
                           'cannot', 'could', 'dear', 'did', 'do', 'does', 'either', 'else', 'ever', 'every',
                           'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers', 'him', 'his',
                           'how', 'however', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least', 'let',
                           'like', 'likely', 'may', 'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor',
                           'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather', 'said',
                           'say', 'says', 'she', 'should', 'since', 'so', 'some', 'than', 'that', 'the', 'their',
                           'them', 'then', 'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us',
                           'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who',
                           'whom', 'why', 'will', 'with', 'would', 'yet', 'you', 'your', 've', 're', 'rt'])
    #turn list into set for faster search
    stop_words = set(stop_words)
    return stop_words