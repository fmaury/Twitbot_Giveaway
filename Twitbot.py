import tweepy
import sys
import random
import time
import os

if not "CONSUMER_KEY" in os.environ or not "CONSUMER_SECRET" in os.environ or not "CONSUMER_SECRET" in os.environ or not "ACCESS_SECRET" in os.environ :
  print ("Missing environnement variable !")
  sys.exit(0)
consumer_key = os.environ["CONSUMER_KEY"]
consumer_secret = os.environ["CONSUMER_SECRET"]
access_token = os.environ["ACCESS_TOKEN"]
access_secret = os.environ["ACCESS_SECRET"]
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

def usage() :
    print ("Usage: python Twitbot.py [argument] [nb of tweet]\nThe first argument must be a hashtag or a keyword (trend or followback) and the second must be an int.")
    sys.exit(0)

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
    #print (status.text)
    print (status.retweet_count)


def taff(searchRequest) :
    list_names = list()
    for status in searchRequest:
        uid = status.id
        nbRT = int(status.retweet_count);
        texte = status.text.split(' ')
        printTweetInfos(status)
        if (nbRT > 5 and hashtag.lower() != "concours" and hashtag.lower() != "#concours") \
                or (nbRT > 1000 and (hashtag.lower() == "concours" or hashtag.lower() == "#concours")) :
            try :
                api.create_favorite(uid)
            except Exception:
                print ("Already liked !")
            try :
                api.retweet(uid)
            except Exception:
                print ("Already RT !")
        if nbRT > 1000 :
            follow(status._json['user']['screen_name']) 
            for names in texte:
                if names and names[0] and names[0] == '@':
                    follow(names[1:])
        del list_names[:]
        print("################################################################")
        ####### ACTIVER APRES PHASE TEST #######
        time.sleep(random.randrange(2, 10, 1))


my_infos = api.me()
my_id = my_infos._json['id']
if len(sys.argv) < 2 :
  usage()
hashtag = sys.argv[1]
if len(sys.argv) < 3 and hashtag is not 'followback' :
  usage()
if sys.argv[2].isdigit() == False :
  usage()
if hashtag == 'followback' :
    for follower in api.followers(my_id):
        follow(follower._json['screen_name'])
        print(follower._json['screen_name'])
else :
    if hashtag == 'trend' :
        print ("Trend: " + api.trends_place(23424819)[0]['trends'][0]['query'])
        hashtag = '#' + api.trends_place(23424819)[0]['trends'][0]['query']

    searchRequest = tweepy.Cursor(api.search, q=hashtag, lang='fr').items(int(sys.argv[2]))
    taff(searchRequest)   
