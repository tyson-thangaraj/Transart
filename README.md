# Transart-Team
Fan Xiangting; He Ping; Song Youtong; Wang Jiandong; Zhao Zeyu

There are two parts of this project: back-end and front-end.
Financial Eye’s goal is to recommend news articles published in different news websites via the topics of BBC news that users are browsing. The key feature of our system is to show different visions based on the same story. 

#Financial_Eye -- Back-End

What we used:
* [Python](https://www.python.org)
* [Django](https://www.djangoproject.com)
* [Django Rest Framework](http://www.django-rest-framework.org)
* [PostgreSql](https://www.postgresql.org)
* [redis&celery](http://www.celeryproject.org)

### 1. accounts
User login / register

### 2. articles
This app is used to fetch news througg Rss feeds and save them to the database.

### 3. articlematch
This app is used to calculate the similarity of news.

#Android -- Front-End

# How to use
Clone the whole project using the following commands:
    
    $ git clone git@github.com:ucd-nlmsc-teamproject/Transart.git

### 1. fetch news with reis & celery
    one terminal:
    $ redis-server &
    another terminal:
    $ python manage.py celeryd -l info -B -c 5

### 2. start the server
    $ python manage.py runserver

### 3. Android
    Generate an apk file and install it.

# code upload
git add filename
git commit -m "commit message"
git push git@github.com:ucd-nlmsc-teamproject/Transart.git
