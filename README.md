# Giveaway Twitter bot
This Bot can be used to do multiple things as:
- retweet specific hashtag
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
python twittbot_launcher.py --help
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

