# Giveaway Twitter bot
This Bot can be used to do multiple things as:
- tweet a text and/or an image
- retweet some tweet containig specific hashtag
- play to giveaway contest
- retweet trending hashtag
- stole a tweet to someone and post it
- follow back your followers

## Install

`$ pip install -r requirement.txt`

## Add your token in tokens.json :

```
{
  "first_account": {
    "API_KEY" : "",
    "API_SECRET" : "",
    "ACCESS_TOKEN" : "",
    "ACCESS_SECRET" : ""
  },
  "second_account": {
    "API_KEY" : "",
    "API_SECRET" : "",
    "ACCESS_TOKEN" : "",
    "ACCESS_SECRET" : ""
  }
}
```
## Usage
```
$ python twittbot_launcher.py --help

Missing: You must choose an account from tokens.json unsing the -a option

usage: twittbot_launcher.py [-h] [-a ACCOUNT] [-m HASHTAG] [-c] [-t] [-s]
                            [-n NUMBERS] [-p POST] [-i IMAGE] [-f]

optional arguments:
  -h, --help            show this help message and exit
  -a ACCOUNT, --account ACCOUNT
                        Select this account
  -m HASHTAG, --hashtag HASHTAG
                        Request tweets with this hashtag in it
  -c, --contest         Play to twitter contests and giveaways
  -t, --trend           Use twitter trends instead of a specific hashtag
  -s, --stole           Stole someone tweet in the top trend section
  -n NUMBERS, --numbers NUMBERS
                        Number of tweets the script will request
  -p POST, --post POST  Post a tweet from a specified file (can be used with
                        "-i" option)
  -i IMAGE, --image IMAGE
                        Post an image from a specified file (can be used with
                        "-p" option)
  -f, --followback      Follow back people that follow you
```

## Config
You can modify the config in this file

Don't forget to create manually the '/var/log/twittbot.log' file if you are not root and give you the right permissions

If you choose another langage than "fr" don't forget to change the giveaway_word
```buildoutcfg
# In which file the log must go
logfile: '/var/log/twittbot.log'

# Tweet's langage. 'fr' for French 'en' for English...
lang : 'fr'

# Trends on twitter by region, you can find the woeid on http://www.woeidlookup.com/
# Exemple : France is 23424819
woeid : 23424819

# Number of retweet nedded to retweet a tweet for the -m (hashtag) mod
nb_rt_hashtag : 5

# Number of retweet needed to play to a contest for the -c (contest) mod
nb_rt_contest : 500

# Maximum number of month (compared to the current date) the tweet mustn't exceed to be processed
max_month : 1

# Maximum number of followers the victim should have for stealing his tweet
nb_follower_stole: 50

# Word used to search for giveaway tweet could be giveaway, contest, concours ect...
giveaway_word: 'concours'
```

## Example

Get 10 tweet (default value) about PSG and retweet those with more than 5 RT (it's in the config file)
```
python3 twittbot_launcher.py -a first_account -m psg
```

Get 20 trending tweet in France (it's in the config file) and retweet those with more than 5 RT (it's in the config file)
```
python3 twittbot_launcher.py -a first_account -t -n 20
```

Play to giveaway contest using 'concours' as keyword (it's in the config file)
```
python3 twittbot_launcher.py -a second_account -c 
```


Followback each people who follow first_account
```
python3 twittbot_launcher.py -a first_account -f
```


Stole a trending tweet in France (it's in the config file) to someone who are less than 50 followers (it's in the config file) and post it using first_account account
```
python3 twittbot_launcher.py -a first_account -s
```


Tweet the text in /root/to/file
```
python3 twittbot_launcher.py -a first_account -p /root/to/file
```

Tweet the image in /root/to/image
```
python3 twittbot_launcher.py -a first_account -i /root/to/image
```


Tweet the text in /root/to/file and post the image in /root/to/image
```
python3 twittbot_launcher.py -a first_account -p /root/to/file -i /root/to/image
```
