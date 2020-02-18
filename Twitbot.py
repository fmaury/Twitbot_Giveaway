# -*- coding: utf-8 -*-
import tweepy
import yaml
import sys
import random
import time
import datetime
import os
import argparse
import json

def getapi():
    token = yaml.load(open("./token.yaml", 'r'), Loader=yaml.Loader)
    consumer_key = token["CONSUMER_KEY"]
    consumer_secret = token["CONSUMER_SECRET"]
    access_token = token["ACCESS_TOKEN"]
    access_secret = token["ACCESS_SECRET"]
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return(tweepy.API(auth))

def follow(name) :
    try : 
        print (name + " is now my friend !")
        api.create_friendship(name) 
    except Exception:
        print (name + " is already my firend :(")

def get_username(api, num) :
    return api.get_user(api.followers_ids(api.me()._json['id'])[num])._json["screen_name"]

def tag_someone(status, api) :
    api.update_status('@' + status._json["entities"]["user_mentions"][0]["screen_name"] + ' @' + get_username(api, 21) + ' @' + get_username(api, 42), status._json["entities"]["user_mentions"][0]['id'])

def printTweetInfos(status) :
    print("Usernamename tweet : " + status._json['user']['screen_name'])
    try :
        print ("Original username tweet" + status._json["entities"]["user_mentions"][0]["screen_name"])
    except :
        print ("No original username tweet")
    print ("This tweet has " + str(status.retweet_count) + " RT")

def tooOld(status):
    month = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
    if hasattr(status, 'retweeted_status'):
        date = status._json['retweeted_status']['created_at']
    else : 
        date = status._json['created_at']
    d = datetime.date.today()
    if d.month - month[date.split()[1]] <= int(config['monthMax']) :
        return (0)
    return (1)

def taff(api, hashtag, numbers) :
    print ("Process " + str(numbers) + " tweets with the hashtag " + hashtag)
    searchRequest = tweepy.Cursor(api.search, q=hashtag, lang=str(config['lang']), tweet_mode="extended").items(numbers)
    for status in searchRequest:
        time.sleep(random.randrange(2, 10, 1))
        if tooOld(status):
            continue
        uid = status.id
        nbRT = int(status.retweet_count)
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
        if (nbRT > int(config['nbRtLikeRt']) and hashtag.lower().find("concour") == -1) \
                or (nbRT > int(config['nbRtFollow']) and hashtag.lower().find("concour") > -1) :
            try :
                api.create_favorite(uid)
            except Exception:
                print ("Already liked !")
            try :
                api.retweet(uid)
            except Exception:
                print ("Already RT !")
        if nbRT > int(config['nbRtFollow']) :
            try :
                follow(status._json["entities"]["user_mentions"][0]["screen_name"])
            except :
                follow(status._json['user']['screen_name']) 
            for names in texte:
                if names and names[0] == '@':
                    if names[:-1] == '.' or names[:-1] == ',':
                        names = names[:-1]
                    follow(names)
                    print ("Name in the tweet following : " + names)
            # tag_someone(status, api)
        print("################################################################")

def followback(api) :
    my_id = api.me()._json['id']
    userlist = api.followers_ids(my_id)
    for follower in userlist:
        time.sleep(random.randrange(2, 5, 1))
        follow(follower)

def trend(api, numbers) :
    taff(api, api.trends_place(int(config['woeid']))[0]['trends'][0]['query'], numbers)   

def stole(api) :
    hashtag = api.trends_place(int(config['woeid']))[0]['trends'][0]['query']
    searchRequest = tweepy.Cursor(api.search, q=hashtag, lang=str(config['lang']), tweet_mode="extended").items(50)
    for status in searchRequest :
        if int(status._json["user"]["followers_count"]) > 200 :
            print ("This user has " + str(status._json["user"]["followers_count"]) + " followers it's risky we'll try another tweet")
            continue
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
        if len(tweet) > 100 :
            print("This tweet is too long: " + str(len(tweet)))
            continue
        if tweet.find('@') != -1 :
            print("Someone is mention in this tweet"))
            continue
        api.update_status(tweet.encode('utf-8'))
        print ("This user as only " + str(status._json["user"]["followers_count"]) + "followers so we use his tweet: " + tweet.encode('utf-8'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--followback", help="Follow back people that follow you", action='store_true')
    parser.add_argument("-t", "--trend", help="Use twitter trends instead of a specific hashtag", action='store_true')
    parser.add_argument("-s", "--stole", help="Stole someone tweet in the top trend section", action='store_true')
    parser.add_argument("-m", "--hashtag", help="Request tweets with this hashtag in it", action='store')
    parser.add_argument("-n", "--numbers", help="Number of tweets the script will request", action='store', default=10, type=int)
    args = parser.parse_args()
    if not args.followback and not args.trend and not args.hashtag and not args.stole :
        parser.print_help()
        sys.exit() 
    config = yaml.load(open("./config.yaml", 'r'), Loader=yaml.Loader)
    api = getapi()
    if args.followback :
        followback(api)
    if args.trend :
        trend(api, args.numbers)
    if args.hashtag :
        taff(api, args.hashtag, args.numbers)
    if args.stole :
        stole(api)
