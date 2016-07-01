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
    elif "ifeng" in url:
        source = "Ifeng"
    elif "sina" in url:
        source = "Sina"

    article.nlp()
    keywords = article.keywords

    return [title, sub_title, news_content, date, keywords, source, image]