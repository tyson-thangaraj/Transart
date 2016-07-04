__author__ = 'fanfan'

from datetime import timedelta, datetime
import sys
import urllib

from celery.schedules import crontab
from celery.task import periodic_task, task
from django.shortcuts import get_object_or_404
from django.utils.timezone import utc
import feedparser
from celery.exceptions import SoftTimeLimitExceeded, TimeLimitExceeded, WorkerShutdown
import redis

from articles.function import createArticleByUrl
from articles.models import Article
#------ google translate --------
from googleapiclient.discovery import build

#read RSS feed every 15mins
#@periodic_task(run_every=crontab(minute='59,14,29,44'), time_limit=14 * 60, soft_time_limit=14 * 50 - 5, expires=60)
@periodic_task(run_every=timedelta(minutes=1), expires=60)
def scrapAll():
    lock_id = "scrapAll"
    have_lock = False
    my_lock = redis.Redis().lock(lock_id, timeout=30 * 60)
    try:
        have_lock = my_lock.acquire(blocking=False)
        if have_lock:
            print(lock_id + " lock acquired!")

            # scrapRSSFeed('http://www.chinadaily.com.cn/rss/world_rss.xml')
            # scrapRSSFeed('http://feeds.bbci.co.uk/news/business/rss.xml')
            # scrapRSSFeed('http://feeds.nytimes.com/nyt/rss/Business')
            # scrapRSSFeed('http://feeds.reuters.com/reuters/businessNews')
            scrapRSSFeed('http://rss.sina.com.cn/roll/finance/hot_roll.xml')
            #scrapRSSFeed('feed://rss.huanqiu.com/finance/view.xml')
            #scrapRSSFeed('http://news.baidu.com/n?cmd=1&class=finannews&tn=rss')
            scrapRSSFeed('http://www.people.com.cn/rss/finance.xml')


        else:
            print(lock_id + " is locked by another worker!")
    except SoftTimeLimitExceeded:
        print('scrapAll soft time limit exceeded!')

    except (TimeLimitExceeded, WorkerShutdown):
        print('scrapAll hard time limit exceeded!')

    # except:
    #     print("Unexpected error:", sys.exc_info()[0])

    finally:
        if have_lock:
            print(lock_id + " released!")
            my_lock.release()


def scrapRSSFeed(feed):
    d = feedparser.parse(feed)

    for item in d['entries']:

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
            get_object_or_404(Article, url=url)
        except:
            try:
                print("create started.....")
                article = createArticleByUrl(url)
                article.save()

            except Exception as err:
                print(err)
                print("Failed adding article " + url)
                pass
            else:
                print("Add New Article:" + article.Headline)

    print(feed + " Done!")


