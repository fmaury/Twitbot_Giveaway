import tweepy

import random
import datetime
import time


class Twittbot:
    def __init__(self, config=None):

        self.config = config

        self.api = None

        self.logfile = '/var/log/twittbot.log'

    """ Log a message """
    def msg_log(self, message):
        timestamp = datetime.datetime.now()
        with open(self.logfile, 'a+') as logfile:
            logfile.write(f'[{timestamp}] {message}')

    """ Connect to the twitter api """
    def connect_api(self, consumer_key=None, consumer_secret=None, access_token=None, access_secret=None):
        self.api = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.api.set_access_token(access_token, access_secret)

    """ Follow a twitter account """
    def follow(self, name):
        try:
            self.msg_log(name + " is now followed.")
            self.api.create_friendship(name)
        except Exception as e:
            self.msg_log(f'{name} is already my friend :(, can\'t follow him: {e}')

    """ Followw back the users who followed your account """
    def followback(self):
        my_id = self.api.me()._json['id']
        userlist = self.api.followers_ids(my_id)
        for follower in userlist:
            time.sleep(random.randrange(2, 5, 1))
            self.follow(follower)

    #   def get_username(api, num):
    #       return self.api.get_user(self.api.followers_ids(self.api.me()._json['id'])[num])._json["screen_name"]

    #   def tag_someone(status, api):
    #       self.api.update_status('@' + status._json["entities"]["user_mentions"][0]["screen_name"] + ' @' + get_username(api, 21) + ' @' + get_username(api, 42),
    #                         status._json["id"])

    """ Write infos about the processed twwet."""
    def print_tweet_infos(self, status, tweet):
        try:
            self.msg_log(f'Tweet write by {status._json["entities"]["user_mentions"][0]["screen_name"]}. Has {str(status.retweet_count)} RTs')
        except:
            self.msg_log(f'Tweet write by {status._json["user"]["screen_name"]}. Has {str(status.retweet_count)} RTs')
        self.msg_log(tweet.encode('utf-8'))

    """ Check if the tweet is not too old """
    def too_old(self, status):
        month = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
        if hasattr(status, 'retweeted_status'):
            date = status._json['retweeted_status']['created_at']
        else:
            date = status._json['created_at']
        d = datetime.date.today()
        if d.month - month[date.split()[1]] <= int(self.config['monthMax']):
            return False
        return True

    """ Send trends tweet to the process_retweet function """
    def trend(self, numbers):
        self.process_retweet(self.api.trends_place(int(self.config['woeid']))[0]['trends'][0]['query'], numbers)

    """ Get some trends tweet then look if the user has few followers and tweet it like it was you that posted that """
    def stole(self):
        hashtag = self.api.trends_place(int(self.config['woeid']))[0]['trends'][0]['query']
        search_request = tweepy.Cursor(self.api.search, q=hashtag + ' -filter:retweets', lang=str(self.config['lang']), tweet_mode="extended").items(50)
        for status in search_request:
            if int(status._json["user"]["followers_count"]) > 200:
                self.msg_log("This user has " + str(status._json["user"]["followers_count"]) + " followers it's risky we'll try another tweet")
                continue
            if hasattr(status, 'retweeted_status'):
                try:
                    tweet = status.retweeted_status.extended_tweet["full_text"]
                except Exception:
                    tweet = status.retweeted_status.full_text
            else:
                try:
                    tweet = status.extended_tweet["full_text"]
                except:
                    tweet = status.full_text
            if len(tweet) > 140:
                self.msg_log("This tweet is too long: " + str(len(tweet)))
                continue
            if tweet.find('@') != -1:
                self.msg_log("Someone is tagged in this tweet")
                continue
            self.api.update_status(tweet.encode('utf-8'))
            self.msg_log("The user " + str(status._json["user"]["screen_name"]) + " as only " + str(
                status._json["user"]["followers_count"]) + "followers so we use his tweet: " + tweet.encode('utf-8'))
            break

    ############################################################################### MAIN PROCESS ###############################################################################

    """ Return the complete tweet """
    @staticmethod
    def __return_tweet(status):
        if hasattr(status, 'retweeted_status'):
            try:
                tweet = status.retweeted_status.extended_tweet["full_text"]
            except:
                tweet = status.retweeted_status.full_text
        else:
            try:
                tweet = status.extended_tweet["full_text"]
            except:
                tweet = status.full_text
        return tweet

    def __retweet_like_handler(self, status, hashtag):
        if (int(status.retweet_count) > int(self.config['nbRtLikeRt']) and hashtag.lower().find("concour") == -1) \
                or (int(status.retweet_count) > int(self.config['nbRtFollow']) and hashtag.lower().find("concour") > -1):
            try:
                self.api.create_favorite(status.id)
            except Exception as e:
                self.msg_log(f"Already liked !: {e}")
            try:
                self.api.retweet(status.id)
            except Exception as e:
                self.msg_log(f"Already RT !: {e}")
                return False
        return True

    """ Foolow account and tagged account in the tweet """
    def __follow_accounts(self, status, tweet):
        try:
            self.follow(status._json["entities"]["user_mentions"][0]["screen_name"])
        except:
            self.follow(status._json['user']['screen_name'])
        for names in tweet.split(' '):
            if names and names[0] == '@':
                if names[:-1] == '.' or names[:-1] == ',':
                    names = names[:-1]
                self.follow(names.encode('utf-8'))
                self.msg_log(f'The user {names.encode("utf-8")} tag in the tweet was followed.')

    """ Get tweets, sort, follow and like them """
    def process_hashtag(self, hashtag, numbers):
        self.msg_log("START :: Looking for " + str(numbers) + " tweets containing " + hashtag)
        search_request = tweepy.Cursor(self.api.search, q=hashtag, lang=str(self.config['lang']), tweet_mode="extended").items(numbers)
        for status in search_request:
            time.sleep(random.randrange(2, 10, 1))
            if self.too_old(status):
                continue
            tweet = self.__return_tweet(status)
            self.print_tweet_infos(status, tweet)
            if not self.__retweet_like_handler(status, hashtag):
                continue
            if int(status.retweet_count) > int(self.config['nbRtFollow']):
                self.__follow_accounts(status, tweet)
                # tag_someone(status, self.api)
            self.msg_log(f"END :: Process hashtag {hashtag} over.")
