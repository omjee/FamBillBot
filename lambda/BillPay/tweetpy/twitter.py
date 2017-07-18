# -*- coding: utf-8 -*-

import json
from requests_oauthlib import OAuth1Session

SEARCH_USER_URL = 'https://api.twitter.com/1.1/users/search.json'
SEARCH_TWITTER_URL = 'https://api.twitter.com/1.1/search/tweets.json'
TRENDING_TOPICS_URL = 'https://api.twitter.com/1.1/trends/place.json'

class ConnectionError(Exception):
    pass

class Twitter(object):
    API_KEY = 'OnyQPj2Frhkg7yAcjCIQ3LPdt'
    API_SECRET = 'YdR3mF8XPYuERZG0rIh8V3G5ydr20PNGHIEzrKCUiCrzkV2kEU'
    ACCESS_TOKEN = '2889095846-RJ9xtphowlos7leiG4pALVUrtx8Ue6NM96uYe5F'
    ACCESS_TOKEN_SECRET = 'ajYzleo2eaQrUqLcJGyaNsClAjRJv9jMpbzP4XpAbnELB'

    def __init__(self):
        self.session = OAuth1Session(
        self.API_KEY,
        self.API_SECRET,
        self.ACCESS_TOKEN,
        self.ACCESS_TOKEN_SECRET
    )

    def search_user(self, user):
        '''Return a list of tuple with format (user, description, location, tweets, following, followers, favorites)'''
        user_list = []
        try:
            response = self.session.get(SEARCH_USER_URL + ("?q=%s" % user))
        except:
            raise ConnectionError('Connection failed!')
        users = json.loads(response.content)
        for user in users:
            user_list.append((user['name'], user['description'], user['location'], user['statuses_count'], user['friends_count'], user['followers_count'], user['favourites_count']))
        return user_list

    def search_tweet(self, keyword, n=15, max_id=None):
        '''Return a list of tuple with format (user, tweet)'''
        tweet_list = []
        try:
            response = self.session.get(SEARCH_TWITTER_URL + ("?q=%s" % keyword))
        except:
            raise ConnectionError('Connection failed!')
        tweets = json.loads(response.content)
        for tweet in tweets['statuses']:
            tweet_list.append((tweet['user']['name'], tweet['text']))
        return tweet_list


    def get_trending_topics(self, region=1):
        '''Return a list with trending topics of a given region. for list complete with region access: https://developer.yahoo.com/geo/geoplanet/guide/concepts.html'''
        trending_topics = []
        try:
            response = self.session.get(TRENDING_TOPICS_URL + ("?id=%s" % region))
        except:
            raise ConnectionError('Connection failed!')
        trends = json.loads(response.content)[0]["trends"]
        for trend in trends:
            trending_topics.append(trend['name'])
        return trending_topics
