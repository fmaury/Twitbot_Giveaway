# -*- coding: utf-8 -*-
import yaml
import json
import sys
import argparse

from pathlib import Path
from Twittbot import Twittbot

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--account", help="Select this account", action='store')
    parser.add_argument("-m", "--hashtag", help="Request tweets with this hashtag in it", action='store')
    parser.add_argument("-c", "--contest", help="Play to twitter contests and giveaways", action='store_true')
    parser.add_argument("-t", "--trend", help="Use twitter trends instead of a specific hashtag", action='store_true')
    parser.add_argument("-s", "--stole", help="Stole someone tweet in the top trend section", action='store_true')
    parser.add_argument("-n", "--numbers", help="Number of tweets the script will request", action='store', default=10, type=int)
    parser.add_argument("-p", "--post", help='Post a tweet from a specified file (can be used with "-i" option)', action='store')
    parser.add_argument("-i", "--image", help='Post an image from a specified file (can be used with "-p" option)', action='store')
    parser.add_argument("-f", "--followback", help="Follow back people that follow you", action='store_true')
    args = parser.parse_args()
    if not args.account:
        print('Missing: You must choose an account from tokens.json unsing the -a option\n', file=sys.stderr)
        parser.print_help()
        sys.exit()

    if not args.followback and not args.trend and not args.hashtag and not args.stole and not args.contest and not args.post and not args.image:
        parser.print_help()
        sys.exit()
    with open(f'{Path(__file__).parents[0]}/tokens.json', 'r') as json_file:
        tokens = json.load(json_file)
        if args.account not in tokens.keys():
            print(f'{args.account} is not in the token.json file, choose one of this account: {", ".join(tokens.keys())}', file=sys.stderr)
            sys.exit()
        consumer_key = tokens[args.account]["API_KEY"]
        consumer_secret = tokens[args.account]["API_SECRET"]
        access_token = tokens[args.account]["ACCESS_TOKEN"]
        access_secret = tokens[args.account]["ACCESS_SECRET"]

    config = yaml.load(open(f"{Path(__file__).parents[0]}/config.yaml", 'r'), Loader=yaml.Loader)

    twittbot = Twittbot(args.account, config)
    twittbot.connect_api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_secret=access_secret)
    if args.followback:
        twittbot.followback()
    if args.trend:
        twittbot.trend(args.numbers)
    if args.contest:
        twittbot.handle_contest(args.numbers)
    if args.hashtag:
        twittbot.handle_hashtag(args.hashtag, args.numbers)
    if args.stole:
        twittbot.stole()
    if args.post or args.image:
        twittbot.tweet(args.post, args.image)
