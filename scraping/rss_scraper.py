import requests
import sys
from bs4 import BeautifulSoup
import json
from pprint import pprint
import random
from newspaper import Article
from sentiment_analysis import sentiment_analysis_helper
import feedparser
import pickle
import time

#rss_list = ['https://feeds.feedburner.com/CoinDesk'] # list of feeds to pull down

rss_list = [#'https://reddit.com/r/bitcoin.rss',
            'https://feeds.feedburner.com/CoinDesk',
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

def save_obj(obj, name ):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def show_urls():
    for feed in rss_list:
        d = feedparser.parse(feed)
        try:
            e = load_obj(d.feed.title)
            print(e)
        except (OSError, IOError) as e:
            f = {}
            save_obj(f,d.feed.title)
            e = load_obj(d.feed.title)
            print(e)


def collect_urls():
    for feed in rss_list:
        d = feedparser.parse(feed)
        # create file if it doesn't exist, if it does, open it
        try:
            e = load_obj(d.feed.title)
        except (OSError, IOError) as e:
            f = {}
            save_obj(f,d.feed.title)
            e = load_obj(d.feed.title)

        for post in d.entries:
            article = Article(post.link)
            from newspaper.article import ArticleException, ArticleDownloadState
            print(post)

            p = {
                "title": post.title,
                "link": post.link,
                "date": post.published
            }
            if ("https://www.google.com/url?rct" in post.link):
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
                p["sa_val"] = sentiment_analysis_helper(article.text)
                e[p["title"]] = p
                save_obj(e, d.feed.title)
            except:
                p["sa_val"] = "error"
                e[p["title"]] = p
                save_obj(e, d.feed.title)
        print(e)

def save_urls():
    e = {}
    for feed in rss_list:
        d = feedparser.parse(feed)
        print(d)
        save_obj(e,d.feed.title)

def main():
    collect_urls()
    show_urls()

main()