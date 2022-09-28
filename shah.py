import json
import configparser
from typing import List
# import pprint
import tweepy

# read config 
config = configparser.ConfigParser()
config.read('config.ini')

CONSUMER_KEY = config['twitter']['CONSUMER_KEY']
CONSUMER_SECRET = config['twitter']['CONSUMER_SECRET']
ACCESS_TOKEN = config['twitter']['ACCESS_TOKEN']
ACCESS_SECRET = config['twitter']['ACCESS_SECRET']

# authenticate
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# pp = pprint.PrettyPrinter(indent=4)

def get_tweets(keyword: str) -> List[str]:
  all_tweets = []

  for tweet in api.search_tweets(q=keyword, lang='en', count=2, result_type="mixed", tweet_mode="extended"):
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


tweets = get_tweets('covid19')
parsedTweet = parsingTweets(tweets)

for tweet in parsedTweet:
  print(json.dumps(tweet, indent=2))

# print(json.dumps(temp, indent=4))