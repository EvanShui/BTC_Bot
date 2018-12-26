import json
import urllib3
import pandas as pd
import praw
from datetime import datetime
from keys.api_keys import *
http = urllib3.PoolManager()

def scrape_reddit():
    """
    Scrape for Reddit posts with PushShift API

    Input:
    start_time (int): left date bound for where to start gathering reddit posts
    end_time (int): right date bound (in days) for where to stop gathering
    reddit posts
    num_entries (int): Number of entries to gather 

    Output:
    list of reddit posts
    """
    reddit = praw.Reddit(client_id=reddit_id,
            client_secret=reddit_secret,
            user_agent=reddit_user_agent)
    for submission in reddit.subreddit('btc').hot(limit=10):
        print(submission.title)

if __name__ == '__main__':
    scrape_reddit()
