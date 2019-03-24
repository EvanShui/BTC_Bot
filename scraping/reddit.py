import json
import urllib3
import pandas as pd
import praw
import pprint
from datetime import datetime, timedelta
from keys.api_keys import *

# global variables
redObj_id = 0

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, praw.models.Submission):
            return super(MyEncoder, self).default(obj)
        return obj.__dict__

def push_shift(start_time, end_time):
    """
    Scrape for Reddit posts with PushShift API

    Input:
    start_time (int): left date bound for where to start gathering reddit
    posts. Time measured in number of days in the past relative to current
    date.
    end_time (int): right date bound for where to stop gathering. Time measured in number of days in the past relative to current
    date.

    reddit posts

    Output:
    list of reddit IDs
    """

    pushshift_url = (
        "https://api.pushshift.io/reddit/search/submission/?subreddit=btc&sort=desc&sort_type=created_utc&after={end}d&before={start}d&size=500".format(start
            = start_time, end=end_time)
    )
    print(pushshift_url)
    http = urllib3.PoolManager()
    response = http.request('GET', pushshift_url)
    reddit_posts = json.loads(response.data.decode('utf-8'))['data']

    # extract just the title from each post in the list of reddit posts
    ids = [post['id'] for post in reddit_posts]
    return ids

def scrape_reddit_post(id_num):
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
    counter = 0
    # Creating pretty print object
    pp = pprint.PrettyPrinter(indent = 4)
    reddit = praw.Reddit(client_id=reddit_id,
            client_secret=reddit_secret,
            user_agent=reddit_user_agent)
    reddit.config.store_json_result = True
    submission = reddit.submission(id = id_num)
    return(submission)

def get_reddit_ids():
    id_lst = []
    counter = 0
    start = datetime.now()
    # the date BTC was released to the public
    end = datetime(2010, 10, 1)
    num_days = (start-end).days - 900
    print("gathering reddit ids")
    while num_days > 0 and counter < 700:
        if num_days < 50:
            start_ind = 50 - num_days
        else:
            start_ind = num_days - 50
        id_lst += push_shift(start_ind, num_days) 
        print("scraped {} reddit posts after: {} before: {}".format(counter, num_days, start_ind))
        counter += 50
        num_days -= 50
        print("printing reddit object titles")
    return(id_lst)

if __name__ == '__main__':
    redObj_lst = []
    id_lst = get_reddit_ids()
    with open("reddit_id.json", "w+") as f:
        json.dump(id_lst, f)
    for id_num in id_lst:
        redObj_lst.append(scrape_reddit_post(id_num))
    for obj in redObj_lst:
        print("{}:".format(redObj_id), obj.title)
        redObj_id += 1

