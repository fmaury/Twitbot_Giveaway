import tweepy

import random
import datetime
import time
from pathlib import Path


class Twittbot:
    def __init__(self, account_name=None, config=None):

        self.config = config
        self.account_name = account_name
        self._sleep = 2

        self.api = None

        self.followed = []

    """ Log a message """
    def msg_log(self, message):
        timestamp = datetime.datetime.now()
        with open(self.config['logfile'], 'a+') as logfile:
            logfile.write(f'[{timestamp}] :: {self.account_name} :: {message}\n')

    """ Connect to the twitter api """
    def connect_api(self, consumer_key=None, consumer_secret=None, access_token=None, access_secret=None):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        self.api = tweepy.API(auth)

    """ Follow a twitter account """
    def follow(self, name):
        try:
            self.msg_log(f'{name} is now followed.')
            self.api.create_friendship(name)
        except Exception as e:
            self.msg_log(f'{name} is already my friend :(, can\'t follow him: {e}')

    """ Followw back the users who followed your account """
    def followback(self):
        self.msg_log("START :: Following back people.")
        my_id = self.api.verify_credentials()._json['id']
        user_list = self.api.get_follower_ids(user_id=my_id)
        for follower in user_list:
            time.sleep(random.randrange(2, 5, 1))
            self.follow(follower)
        self.msg_log("START :: Folliw back over.")

    """ Write infos about the processed twwet."""
    def print_tweet_infos(self, status, tweet):
        try:
            self.msg_log(f'Tweet write by {status._json["entities"]["user_mentions"][0]["screen_name"]}. Has {str(status.retweet_count)} RTs')
        except:
            self.msg_log(f'Tweet write by {status._json["user"]["screen_name"]}. Has {str(status.retweet_count)} RTs')
        self.msg_log(tweet)

    """ Check if the tweet is not too old """
    def too_old(self, status):
        month = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
        if hasattr(status, 'retweeted_status'):
            date = status._json['retweeted_status']['created_at']
        else:
            date = status._json['created_at']
        d = datetime.date.today()
        if d.month - month[date.split()[1]] <= int(self.config['max_month']):
            return False
        return True

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

    def __retweet_like_giveaway_handler(self, status):
        try:
            self.api.create_favorite(status.id)
        except Exception as e:
            self.msg_log(f"Already liked !: {e}")
            return False
        try:
            self.api.retweet(status.id)
        except Exception as e:
            self.msg_log(f"Already RT !: {e}")
        return True

    """ Follow account and tagged account in the tweet """
    def __follow_accounts(self, status, tweet):
        try:
            self.follow(status._json["entities"]["user_mentions"][0]["screen_name"])
        except:
            self.follow(status._json['user']['screen_name'])
        for names in tweet.split(' '):
            if names and names[0] == '@':
                if names[:-1] == '.' or names[:-1] == ',':
                    names = names[:-1]
                self.followed.append(names)
                self.follow(names.encode('utf-8'))
                self.msg_log(f'The user {names.encode("utf-8")} tag in the tweet was followed.')

    def __get_username(self):
        my_id = self.api.verify_credentials()._json['id']
        user_list = self.api.get_follower_ids(user_id=my_id)
        if len(user_list) == 0:
            return '@elonmusk'
        user = user_list[random.randint(0, len(user_list) - 1)]
        username = self.api.get_user(user)._json['screen_name']
        self.msg_log(f"STATUS :: Request username in my followers: name @{username} id {user}.")
        return f'@{username}'

    """ Check if people are tagged in the tweet, if yes request in my follower, replace user mentionned with mine and reply to the tweet """
    def __stole_contest_reply(self, status):
        reply_list = []
        if 'retweeted_status' in status._json:
            tweet_id = status._json['retweeted_status']['id']
        else:
            tweet_id = status._json["id"]
        try:
            name = status._json["entities"]["user_mentions"][0]["screen_name"]
        except:
            name = status._json['user']['screen_name']
        self.msg_log(f"STATUS :: Trying to stole a reply to the user {name} and tweet ID {tweet_id}.")
        rep_request = tweepy.Cursor(self.api.search_tweets, q=f'@{name}', since_id=tweet_id, tweet_mode="extended").items(50)
        for rep in rep_request:
            if rep._json['in_reply_to_status_id'] == tweet_id:
                tweet = self.__return_tweet(rep)
                if tweet.count('@') > 1:
                    self.msg_log(f"STATUS :: People tagged in this tweet:  {tweet}.")
                    tweet_split = tweet.split(' ')
                    for word in tweet_split:
                        if word[0] == '@' and word.find(name) == -1 and word not in self.followed:
                            reply_list.append(self.__get_username())
                        else:
                            reply_list.append(word)
                    reply = ' '.join(reply_list)
                    self.msg_log(f"STATUS :: Original tweet modified: {reply}.")
                    self.api.update_status(status=reply, in_reply_to_status_id=tweet_id)
                    break

    """ Get giveaways tweets, sort, follow, retweet and like them """
    def handle_contest(self, numbers):
        self.msg_log(f"START :: Looking for {str(numbers)} giveaways tweets")
        time.sleep(random.randrange(1, self._sleep, 1))
        search_request = tweepy.Cursor(self.api.search_tweets, q=self.config['giveaway_word'], lang=str(self.config['lang']), tweet_mode="extended").items(numbers)
        for status in search_request:
            self.followed = []
            time.sleep(random.randrange(2, 10, 1))
            tweet = self.__return_tweet(status)
            self.print_tweet_infos(status, tweet)
            if self.too_old(status) or int(status.retweet_count) < int(self.config['nb_rt_contest']):
                self.msg_log(f"STATUS :: This tweet is too old or has not enougth retweet")
                continue
            if self.__retweet_like_giveaway_handler(status):
                self.__follow_accounts(status, tweet)
                self.__stole_contest_reply(status)
        self.msg_log(f"END :: Process giveaways tweets over.")

    """ Get tweets from hashtag, sort and retweet them """
    def handle_hashtag(self, hashtag, numbers):
        self.msg_log(f"START :: Looking for {str(numbers)} tweets containing {hashtag}")
        time.sleep(random.randrange(1, self._sleep, 1))
        search_request = tweepy.Cursor(self.api.search_tweets, q=hashtag, lang=str(self.config['lang']), tweet_mode="extended").items(numbers)
        for status in search_request:
            time.sleep(random.randrange(2, 10, 1))
            tweet = self.__return_tweet(status)
            self.print_tweet_infos(status, tweet)
            if self.too_old(status) or int(status.retweet_count) < int(self.config['nb_rt_hashtag']):
                self.msg_log(f"STATUS :: This tweet is too old or has not enougth retweet")
                continue
            try:
                self.api.retweet(status.id)
            except Exception as e:
                self.msg_log(f"Already RT !: {e}")
        self.msg_log(f"END :: Process hashtag {hashtag} over.")

    """ Send trends tweet to the process_retweet function """
    def trend(self, numbers):
        time.sleep(random.randrange(1, self._sleep, 1))
        self.handle_hashtag(self.api.get_place_trends(int(self.config['woeid']))[0]['trends'][0]['query'], numbers)

    """ Get some trends tweet then look if the user has few followers and tweet it like it was you that posted that """
    def stole(self):
        self.msg_log("START :: Looking for a tweet to stole.")
        time.sleep(random.randrange(1, self._sleep, 1))
        hashtag = self.api.get_place_trends(int(self.config['woeid']))[0]['trends'][0]['query']
        search_request = tweepy.Cursor(self.api.search_tweets, q=hashtag + ' -filter:retweets', lang=str(self.config['lang']), tweet_mode="extended").items(50)
        for status in search_request:
            if int(status._json["user"]["followers_count"]) > self.config['nb_follower_stole']:
                self.msg_log("This user has " + str(status._json["user"]["followers_count"]) + " followers it's risky we'll try another tweet")
                continue
            tweet = self.__return_tweet(status)
            if len(tweet) > 140:
                self.msg_log("This tweet is too long: " + str(len(tweet)))
                continue
            if tweet.find('@') != -1:
                self.msg_log("Someone is tagged in this tweet")
                continue
            self.api.update_status(tweet)
            self.msg_log(f'The user {status._json["user"]["screen_name"]} as only {status._json["user"]["followers_count"]} followers so we use his tweet: {tweet}')
            self.msg_log("END :: Tweet stoled (hihi).")
            break

    """ Tet a text an image or both """
    def tweet(self, tweet_file=None, image=None):
        time.sleep(random.randrange(1, self._sleep, 1))
        self.msg_log(f'START :: Tweet something')
        if tweet_file:
            if not Path(tweet_file).exists():
                self.msg_log(f'ERROR :: File {tweet_file} doesn\'t exist')
                return
        if image:
            if not Path(image).exists():
                self.msg_log(f'ERROR :: Image {image} doesn\'t exist')
                return
        if tweet_file and image:
            self.msg_log(f'INFO :: Tweet the text from {tweet_file} with image from {image}')
            with open(tweet_file, 'r') as tweetf:
                tweet = tweetf.read()
                self.api.update_with_media(image, status=tweet)
        elif tweet_file:
            self.msg_log(f'INFO :: Tweet the text from {tweet_file}')
            with open(tweet_file, 'r') as tweetf:
                tweet = tweetf.read()
                self.api.update_status(tweet)
        elif image:
            self.msg_log(f'INFO :: Tweet image from {image}')
            self.api.update_with_media(image)