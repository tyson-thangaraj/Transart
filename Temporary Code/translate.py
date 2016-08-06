from googleapiclient.discovery import build
import feedparser
from bs4 import BeautifulSoup
import newspaper
import urllib
from http.cookiejar import CookieJar
from datetime import timedelta, datetime
from datetime import datetime


# google translate API 
def googleTranslate(text):
    myKey = 'AIzaSyDB5M7vM-gnhG4jKWp6E4PT5Y3GhLAprlE'
    service = build('translate', 'v2',
            developerKey=myKey)

    translatedText = service.translations().list(
      source='zh',
      target='en',
      q = text
      #q=['He said Brexit would "freeze the possibilities of investment in Great Britain or in Europe as a whole". He appealed to the UK prime minister and other EU leaders to ensure an orderly process for the British exit.', 'car']
    ).execute()
    
    return translatedText

def scrapRSSFeed(feed):
    d = feedparser.parse(feed)

    for item in d['entries']:
        print(item['link'])

        if "bbc" in item['link']:
            url = item['id']
            # url = url.replace(".co.uk/", ".com/")
        elif "nytimes" in item['link']:
            url = item['guid']
        elif "sina" in item['link']:
            url=item['link']
            url = url.split('=')[1]
        else:
            url = item['link']

        if '?localLinksEnabled=false' in url:
            url = url.replace('?localLinksEnabled=false', '')

        if '?feedType=RSS&feedName=topNews' in url:
            url = url.replace('?feedType=RSS&feedName=topNews', '')

        # if "?nytimes" in url:
        #     url = urllib.parse.quote(url, '/:')
        url = urllib.parse.quote(url, '/:')


        try:
            print("create started.....")
            getArticleDetailsByUrl(url)
#                 article = createArticleByUrl(url)
#                 article.save()

        except Exception as err:
            print(err)
            print("Failed adding article " + url)
            pass
        else:
            print("Add New Article:" + article.Headline)

    print(feed + " Done!")

# def createArticleByUrl(url):
#     [title, subtitle, body, date, keywords, source, image] = getArticleDetailsByUrl(url)
#     article = createArticleObject(title, subtitle, body, date, keywords, url, "RSS", source, image)
#     return article
    
def getArticleDetailsByUrl(url):
    #print(url)
    print(".................................................................................................................")
    article = newspaper.Article(url)
    print(".................................................................................................................")
    article.download()
    print(".................................................................................................................")
    article.parse()

    print(".................................................................................................................")
    title = article.title
    sub_title=article.meta_description
    # authors = article.authors
    date = article.publish_date

    news_content = article.text
#     image = article.top_image

#     article.nlp()
#     keywords = article.keywords
    print("**************************************************************************************************************************")
    source = "other"
    if "chinadaily" in url:
        page = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(page,"html.parser")
        soup.prettify()
        source = "ChinaDaily"
        tag = soup.find("span", attrs={"class": "greyTxt6 block mb15"}).get_text()
        date = str.split(tag, ':  ')[1]

        from django.utils.timezone import utc
        from datetime import timedelta, datetime
        date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        date = date.replace(tzinfo=utc) - timedelta(hours=7)
    elif "bbc" in url:
        page = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(page,"html.parser")
        soup.prettify()
        source = "BBC"
        newsscripts = str(soup.find("script", attrs={"type": "application/ld+json"}).string)

        from json import loads as JSON
        from django.utils.timezone import utc
        from datetime import timedelta, datetime
        parsed = JSON(newsscripts)
        date0 = parsed['datePublished']
        print(date0)
        date = datetime.strptime(date0, "%Y-%m-%dT%H:%M:%S+01:00")
        print(date)

        # if "GMT" in date:
        #     date = datetime.strptime(date, "%d %B %Y")
        # else:
        #     date = datetime.strptime(date, "%d %B %Y")
        #     local_dt = pytz.timezone('Europe/Dublin').localize(date, is_dst=None)
        #     date = local_dt.astimezone(pytz.utc)
    elif "sina" in url:
        page = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(page,"html.parser",from_encoding="GB18030")
        soup.prettify()
        source = "Sina"
        title = str.split(soup.title.string, '|')[0]
        sub_title = soup.head.find("meta",attrs={"name":"description"}).get('content')
        print("&&&&&&&&&&&&&&&&&&&&&&&&&")
        news_content_list = []
        print(news_content)
        news_content=''
        for tag in soup.find("div", attrs={"id": "artibody"}).find_all("p"):
            if "JavaScript" not in tag.get_text():
                print(tag.get_text())
                print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
                news_content += tag.get_text() + '\n'
                news_content_list.append(tag.get_text())
        
        # translation
#         originalText = [title, sub_title, news_content]
#         original_content = originalText[2]
        print(news_content)
        print("-------")
        print(news_content_list)
        print("-------")
        translatedText = ''

        # for paragraph in news_content_list:
        #     paragraph_translated = googleTranslate(paragraph)
        #     print(paragraph_translated)
           # translatedText += paragraph_translated['translations'][0]
        translatedText = googleTranslate(news_content_list)
        print(translatedText)
        a = ' '
        for item in translatedText['translations']:
            a += item['translatedText'] + '\n'
#         print("-------")
# #         title = translatedText['translations'][0]['translatedText']
# #         sub_title= translatedText['translations'][1]['translatedText']
# #         news_content = translatedText['translations'][2]['translatedText']

# #         keywords = extractKeywords(title)
        
        print(translatedText)
        print(a)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


    #return [title, sub_title, news_content, date, keywords, source, image]
    

#scrapRSSFeed('http://rss.sina.com.cn/roll/finance/hot_roll.xml')

url = 'http://www.bbc.com/news/business-36973936'
getArticleDetailsByUrl(url)