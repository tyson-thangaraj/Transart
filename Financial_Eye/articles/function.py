__author__ = 'fanfan, Jiandong Wang'

import urllib
from datetime import datetime
from bs4 import BeautifulSoup
import nltk
import pytz
from articles.models import Article
import newspaper
from http.cookiejar import CookieJar
from django.utils.timezone import utc
from datetime import timedelta, datetime
#------ google translate --------
from googleapiclient.discovery import build

def createArticleObject(title, subtitle, body, date, keywords, url, type, source, image):
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

    # fetch news using the library newspaper
    article = newspaper.Article(url)
    article.download()
    article.parse()

    #get the title of the news
    title = article.title
    #the description
    sub_title=article.meta_description
    # authors = article.authors
    #the date that the news published. Maybe edited later
    date = article.publish_date

    #get the contents of the news
    news_content = article.text
    image = article.top_image

    article.nlp()
    keywords = article.keywords

    source = "other"
    if "chinadaily" in url:
        #using beautifulsoup to get descrape the html
        page = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(page,"html.parser")
        soup.prettify()
        source = "ChinaDaily"
        # get the published date. the date that the library newspaper got is not what we need.
        tag = soup.find("span", attrs={"class": "greyTxt6 block mb15"})
        if tag != None:
            date_tag = tag.get_text()
            date = str.split(date_tag, ':  ')[1]
            date = datetime.strptime(date, "%Y-%m-%d %H:%M")
            date = date.replace(tzinfo=utc) - timedelta(hours=8)
    elif "bbc" in url:
        #using beautifulsoup to get descrape the html to get the date
        page = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(page,"html.parser")
        soup.prettify()
        source = "BBC"
        #get javascript from html
        newsscripts = str(soup.find("script", attrs={"type": "application/ld+json"}).string)
        #get the published date in javascript
        from json import loads as JSON
        parsed = JSON(newsscripts)
        date = parsed['datePublished']
        # date0 = parsed['datePublished']
        # date = datetime.strptime(date0, "%Y-%m-%dT%H:%M:%S+01:00")

    elif "nytimes" in url:
        source="The New York Times"
        #scrape the html with HTTPCookieProcessor
        cj = CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        p = opener.open(url).read()
        soup = BeautifulSoup(p,"html.parser")
        soup.prettify()
        tag = soup.find("meta", attrs={"name": "ptime"}).get('content')
        date = datetime.strptime(tag, "%Y%m%d%H%M%S")
    elif "reuters" in url:
        source="Reuters"
    elif "sina" in url:
        #using beautifulsoup to get descrape the html to get the date
        page = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(page,"html.parser",from_encoding="GB18030")
        soup.prettify()
        source = "Sina"
        title = str.split(soup.title.string, '|')[0]
        sub_title = soup.head.find("meta",attrs={"name":"description"}).get('content')
        news_content = ' '
        news_content_list = []
        for tag in soup.find("div", attrs={"id": "artibody"}).find_all("p"):
            if "JavaScript" not in tag.get_text():
                # news_content += tag.get_text() + '\n'
                news_content_list.append(tag.get_text())

        # tranlate content
        translated_content = googleTranslate(news_content_list)

        for item in translated_content['translations']:
            news_content += item['translatedText'] + '\n\n'

        # translate title and sub_title    
        originalText = [title, sub_title]
        translatedText = googleTranslate(originalText)

        title = translatedText['translations'][0]['translatedText']
        sub_title= translatedText['translations'][1]['translatedText']

        keywords = extractKeywords(title)
    elif "channelnewsasia" in url:
        source = "Channel NewsAsia"
        #using beautifulsoup to get descrape the html to get the date
        page = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(page,"html.parser")
        soup.prettify()
        tag = soup.find("meta", attrs={"name": "cXenseParse:recs:publishtime"}).get('content')
        date = datetime.strptime(tag, "%Y-%m-%dT%H:%MZ")
    elif "spiegel" in url:
        source = "Spiegel Online International"
    elif "france24" in url:
        source = "France 24"
    elif "asiaone" in url:
        source = "AsiaOne Business"
    elif "cnn.com" in url:
        source = "CNN"
    elif "xinhuanet" in url:
        source = "Xinhua Net"

    return [title, sub_title, news_content, date, keywords, source, image]

#extrack keywords
def extractKeywords(text):
    stop_words = nltk.corpus.stopwords.words('english')
    keywords = []
    tokens = nltk.word_tokenize(text)

    for token in tokens:
        if token not in stop_words:
            keywords.append(token.lower())
    return ", ".join(keywords)

# google translate API 
# NOTE: the IP address of the server must get the permission to run this translation method
def googleTranslate(text):
    # register the translation key
    myKey = 'AIzaSyDB5M7vM-gnhG4jKWp6E4PT5Y3GhLAprlE'
    service = build('translate', 'v2',
            developerKey=myKey)

    translatedText = service.translations().list(
      source='zh',
      target='en',
      q = text
    ).execute()
    
    return translatedText
