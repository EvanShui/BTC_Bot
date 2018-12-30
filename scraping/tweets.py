import tweepy
from keys.credentials import *

try:
    auth = tweepy.OAuthHandler(app_key, app_secret)
    auth.set_access_token(access_token, access_secret)
    print('setting authentication')
    api = tweepy.API(auth)
    print('confirmed authentication')
    for tweet in api.search(q ='bitcoin', count = 50, lang='en'):
        # print("\n----------------\n")
        print(tweet.text)
except:
    print("no tweet")