import requests
import sys
from bs4 import BeautifulSoup
import json
from pprint import pprint
import random

from newspaper import Article
from sentiment_analysis import sentiment_analysis_helper
from sentiment_analysis import sa_everything
from datetime import datetime

import feedparser
import pickle
import time

#rss_list = ['https://feeds.feedburner.com/CoinDesk'] # list of feeds to pull down

rss_list = ['https://feeds.feedburner.com/CoinDesk',
            'https://www.marketwatch.com/rss/newsfinder/AllMarketWatchNews/?p=word&pv=bitcoin&t=bitcoin&dist=sr_rss',
            'https://www.google.com/alerts/feeds/06223710574130131730/16959083728935259576',
            'https://news.bitcoin.com/feed',
            'https://bitcoin.org/en/rss/blog.xml',
            'https://newsbtc.com/feed',
            'https://www.cryptocoinsnews.com/feed',
            'https://blog.blockchain.com/feed',
            'https://Bitcoinist.com/feed',
            'https://blog.kraken.com/rss',
            'https://bitcoinmagazine.com/feed',
            'https://cointelegraph.com/rss/tag/bitcoin'] # list of feeds to pull down

'''
PKL file save/load functions.
Open a dictionary, and save that dictionary to a file
'''
def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

# Used to print out current RSS files, without pulling/using more data
def show_urls():
    for feed in rss_list:
        d = feedparser.parse(feed)
        try:
            e = load_obj(d.feed.title)  # Load each file that corresponds to each feed
            print(e)
        except (OSError, IOError) as e:
            f = {}
            save_obj(f,d.feed.title)    # If file does not exist, create an empty one
            e = load_obj(d.feed.title)
            print(e)

'''
Main function, used to pull available feeds/articles, parse their data, and save
Saves Article Title, link, date (format Y-M-D H:M:S), and SA value
'''
def collect_urls():
    for feed in rss_list:
        d = feedparser.parse(feed)

        '''
        # create file if it doesn't exist, if it does, open it
        try:
            e = load_obj(d.feed.title)
        except (OSError, IOError) as e: # create empty file
            f = {}
            save_obj(f,d.feed.title)
            e = load_obj(d.feed.title)
        '''

        json_file = gen_json(d)
        '''
        TODO: Capture current article ID from sort, and most recent article date
        ID = list size?
        '''

        for post in d.entries:
            article = Article(post.link)
            from newspaper.article import ArticleException, ArticleDownloadState

            '''
            TODO: If post date is before newest article in file, move to next feed
            '''
            p = {
                "id": post.id,  # check this
                "title": post.title,
                "link": post.link,
                "date": format_date(post.published)
                #text field?
            }
            if ("https://www.google.com/url?rct" in post.link): # Fixes Google post URLs to get true article URL
                p["link"] = post.link.split("&url=",1)[1]

            slept = 0
            try:
                article.download()
                while article.download_state == ArticleDownloadState.NOT_STARTED:
                    # Raise exception if article download state does not change after 10 seconds
                    if slept > 9:
                        raise ArticleException('Download never started')
                    time.sleep(1)
                    slept += 1
                # Parse article
                article.parse()
                print(sa_everything(article.text))
                p["sa_val"] = sentiment_analysis_helper(article.text)
            except:
                p["sa_val"] = "error"

            json_file.append(p)

        with open(d.feed.title, 'w+') as f:
            json.dump(json_file, f)

def save_urls():
    e = {}
    for feed in rss_list:
        d = feedparser.parse(feed)
        print(d)
        save_obj(e,d.feed.title)

def test_file_feed():
    for feed in rss_list:
        d = feedparser.parse(feed)
        for post in d.entries:
            article = Article(post.link)
            from newspaper.article import ArticleException, ArticleDownloadState
            slept = 0
            try:
                article.download()
                while article.download_state == ArticleDownloadState.NOT_STARTED:
                    # Raise exception if article download state does not change after 10 seconds
                    if slept > 9:
                        raise ArticleException('Download never started')
                    time.sleep(1)
                    slept += 1
                # Parse article
                article.parse()
                print(sa_everything(article.text))
            except:
                print("Error")
    '''
    #print("Got here")
    d = feedparser.parse('index.html')
    #print(d.feed.title)
    for post in d.entries:
        article = Article(post.link)
        from newspaper.article import ArticleException, ArticleDownloadState
        slept = 0
        try:
            article.download()
            while article.download_state == ArticleDownloadState.NOT_STARTED:
                # Raise exception if article download state does not change after 10 seconds
                if slept > 9:
                    raise ArticleException('Download never started')
                time.sleep(1)
                slept += 1
            # Parse article
            article.parse()
            print(sa_everything(article.text))
        except:
            print("Error")
    '''



def test_sa():
    d = feedparser.parse('https://feeds.feedburner.com/CoinDesk')

    '''
    # create file if it doesn't exist, if it does, open it
    try:
        e = load_obj(d.feed.title)
    except (OSError, IOError) as e: # create empty file
        f = {}
        save_obj(f,d.feed.title)
        e = load_obj(d.feed.title)
    '''

    #json_file = gen_json(d)
    '''
    TODO: Capture current article ID from sort, and most recent article date
    ID = list size?
    '''

    for post in d.entries:
        article = Article(post.link)
        from newspaper.article import ArticleException, ArticleDownloadState

        '''
        TODO: If post date is before newest article in file, move to next feed
        '''
        p = {
            "id": post.id,  # check this
            "title": post.title,
            "link": post.link,
            "date": format_date(post.published)
            # text field?
        }
        if ("https://www.google.com/url?rct" in post.link):  # Fixes Google post URLs to get true article URL
            p["link"] = post.link.split("&url=", 1)[1]

        slept = 0
        try:
            article.download()
            while article.download_state == ArticleDownloadState.NOT_STARTED:
                # Raise exception if article download state does not change after 10 seconds
                if slept > 9:
                    raise ArticleException('Download never started')
                time.sleep(1)
                slept += 1
            # Parse article
            article.parse()
            print(sa_everything(article.text))
            p["sa_val"] = sentiment_analysis_helper(article.text)
        except:
            p["sa_val"] = "error"


# Convert RSS datetime string to something we can use
def format_date(d):
    new_time = datetime.strptime(d,'%a, %d %b %Y %H:%M:%S +0000')
    return new_time.strftime('%Y-%m-%d %H:%M:%S')

def gen_json(d):
    e = []
    '''
    TODO: Append .json to end of file name
    '''
    try:
        with open(d.feed.title, 'r') as f:
            return json.load(f)
    except (OSError, IOError) as e:
        with open(d.feed.title , 'w+') as f:
            json.dump(e, f)
            with open(d.feed.title, 'r') as f:
                return json.load(f)

def main():
    #print(format_date('Sat, 29 Dec 2018 14:01:03 +0000'))
    #test_sa()
    test_file_feed()
    #collect_urls()
    #show_urls()

main()