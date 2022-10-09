import configparser
from typing import List
import tweepy
import pandas as pd

# read config 
config = configparser.ConfigParser()
config.read('config.ini')

# read Twitter Config
CONSUMER_KEY = config['twitter']['CONSUMER_KEY']
CONSUMER_SECRET = config['twitter']['CONSUMER_SECRET']
ACCESS_TOKEN = config['twitter']['ACCESS_TOKEN']
ACCESS_SECRET = config['twitter']['ACCESS_SECRET']

LAST_TWEET_ID = config['filename']['LAST_TWEET_ID_FILENAME']

# authenticate
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

def get_tweets(keyword: str, lastTweetId) -> List[str]:
  all_tweets = []

  # for tweet in api.search_tweets(q=keyword, lang='en', count=10, result_type="mixed", tweet_mode="extended"):
  for tweet in api.search_tweets(q=keyword, lang='en', count=10, result_type="mixed", tweet_mode="extended", since_id=lastTweetId):
    all_tweets.append(tweet)
  
  return all_tweets

# def getPremiumTweets(keyword: str) -> List[str]:
#   premiumTweets = []
#   for tweet in api.search_30_day(label="development", query=keyword, maxResults=10):
#     premiumTweets.append(tweet)
#   return premiumTweets

def parsingTweets(tweets: List) -> List[str]:
  parsedTweets = []

  for tweet in tweets:
    parsedTweets.append({
      "created_at": tweet._json["created_at"],
      "id": tweet._json["id"],
      "full_text": tweet._json["full_text"],
      "username": tweet._json["user"]["name"],
      "handle": tweet._json["user"]["screen_name"],
      "location": tweet._json["user"]["location"],
      "favorite_count": tweet._json["favorite_count"],
      "retweet_count": tweet._json["retweet_count"]
    })
    
  return parsedTweets


def saveLastTweetId(tweets: List):
  id = tweets[-1]["id"]

  fileName = LAST_TWEET_ID
  f = open(fileName, 'w+')
  f.write(str(id))
  f.close()
  return None

def readLastTweetId():
  fileName = LAST_TWEET_ID
  f = open(fileName, "r")
  id = int(f.read())
  return id

tweets = get_tweets('covid19', readLastTweetId())
parsedTweets = parsingTweets(tweets)
saveLastTweetId(parsedTweets)

tweetsDf = pd.DataFrame.from_dict(parsedTweets)
print(tweetsDf.head(10))