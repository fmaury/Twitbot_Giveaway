# -*- coding: utf-8 -*-
import tweepy
import yaml
import sys
import random
import time
import datetime
import os
import pprint


def usage() :
    print ("Usage: python Twitbot.py [argument] [nb of tweet]\n   -The first argument must be a hashtag or a keyword (trend or followback) and the second must be an int.")
    sys.exit(0)

def getapi():
    token = yaml.load(open("./token.yaml", 'r'))
    consumer_key = token["CONSUMER_KEY"]
    consumer_secret = token["CONSUMER_SECRET"]
    access_token = token["ACCESS_TOKEN"]
    access_secret = token["ACCESS_SECRET"]
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return(tweepy.API(auth))

def follow(name) :
    if name[len(name) - 1] == ':' :
        name = name[:len(name) - 1]
        print ("Follow: " + name)
    try : 
        api.create_friendship(name) 
    except Exception:
        print ("Already followed !")

def printTweetInfos(status) :
    print(status._json['user']['screen_name'])
    print (status.retweet_count)
    if status._json['retweeted_status'] : 
        print(status._json['retweeted_status']['created_at'])
    else : 
        print(status._json['created_at'])
    #print (status)

def tooOld(date):
    mois = {"January":1, "Febuary": 2}
    print (date)
    d = datetime.date.today()
    print ("mois: " + str(d.month))
    return (0)

def taff(searchRequest, hashtag) :
    list_names = list()
    for status in searchRequest:
        if tooOld(status._json['created_at']):
            continue

        uid = status.id
        nbRT = int(status.retweet_count);
        if hasattr(status, 'retweeted_status'):
            try:
                tweet = status.retweeted_status.extended_tweet["full_text"]
            except:
                tweet = status.retweeted_status.full_text
        else:
            try:
                tweet = status.extended_tweet["full_text"]
            except :
                tweet = status.full_text
        print (tweet.encode('utf-8'))
        texte = tweet.split(' ')
        printTweetInfos(status)
       # if hashtag == "42genesys" or (nbRT > config['nbRtLikeRt'] and hashtag.lower() != "concours" and hashtag.lower() != "#concours") \
       #         or (nbRT > config['nbRtFollow'] and (hashtag.lower() == "concours" or hashtag.lower() == "#concours")) :
       #     try :
       #         api.create_favorite(uid)
       #     except Exception:
       #         print ("Already liked !")
       #     try :
       #         api.retweet(uid)
       #     except Exception:
       #         print ("Already RT !")
       # if nbRT > config['nbRtFollow'] :
       #     follow(status._json['user']['screen_name']) 
       #     for names in texte:
       #         if names and names[0] and names[0] == '@':
       #             if names[len(names) - 1] != '.' and names[len(names) - 1] != ',':
       #                 follow(names[1:])
       #             else :
       #                 follow(names[1:-1])
       # del list_names[:]
       # print("################################################################")
       # ####### ACTIVER APRES PHASE TEST #######
       # time.sleep(random.randrange(2, 10, 1))
       # time.sleep(1)

if __name__ == "__main__":
    config = yaml.load(open("./config.yaml", 'r'))
    api = getapi()
    hashtag = sys.argv[1]
    if  len(sys.argv) < 2 or (len(sys.argv) < 3 and hashtag != 'followback') :
        usage()
    if hashtag == 'followback' :
        my_infos = api.me()
        my_id = my_infos._json['id']
        for follower in api.followers(my_id):
            follow(follower._json['screen_name'])
            print(follower._json['screen_name'])
        sys.exit(0)
    else :
        if hashtag == 'trend' :
            print ("Trend: " + api.trends_place(23424819)[0]['trends'][0]['query'])
            hashtag = '#' + api.trends_place(23424819)[0]['trends'][0]['query']
    if sys.argv[2].isdigit() == False :
        usage()
    searchRequest = tweepy.Cursor(api.search, q=hashtag, lang='fr', tweet_mode="extended").items(int(sys.argv[2]))
    taff(searchRequest, hashtag)   
