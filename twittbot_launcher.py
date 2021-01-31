# -*- coding: utf-8 -*-
import yaml
import sys
import argparse

from Twittbot import Twittbot

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--followback", help="Follow back people that follow you", action='store_true')
    parser.add_argument("-t", "--trend", help="Use twitter trends instead of a specific hashtag", action='store_true')
    parser.add_argument("-s", "--stole", help="Stole someone tweet in the top trend section", action='store_true')
    parser.add_argument("-m", "--hashtag", help="Request tweets with this hashtag in it", action='store')
    parser.add_argument("-n", "--numbers", help="Number of tweets the script will request", action='store', default=10, type=int)
    args = parser.parse_args()
    if not args.followback and not args.trend and not args.hashtag and not args.stole:
        parser.print_help()
        sys.exit()

    token = yaml.load(open("./token.yaml", 'r'), Loader=yaml.Loader)

    config = yaml.load(open("./config.yaml", 'r'), Loader=yaml.Loader)
    twittbot = Twittbot(config)
    twittbot.connect_api(consumer_key=token["CONSUMER_KEY"], consumer_secret=token["CONSUMER_SECRET"],
                         access_token=token["ACCESS_TOKEN"], access_secret=token["ACCESS_SECRET"])
    if args.followback:
        twittbot.followback()
    if args.trend:
        twittbot.trend(args.numbers)
    if args.hashtag:
        twittbot.process_hashtag(args.hashtag, args.numbers)
    if args.stole:
        twittbot.stole()
