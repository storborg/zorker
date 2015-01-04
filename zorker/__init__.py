import re
import sys

from pprint import pprint
from ConfigParser import RawConfigParser

import tweepy

from .dfrotz import DFrotz


config_section = 'zorker'


def get_api(config):
    consumer_key = config.get(config_section, 'consumer_key')
    consumer_secret = config.get(config_section, 'consumer_secret')
    access_token = config.get(config_section, 'access_token')
    access_token_secret = config.get(config_section, 'access_token_secret')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)


def split_long_tweet(s):
    msg = ''
    for word in s.strip().split(' '):
        if len(msg) + len(word) > 139:
            yield msg
            msg = word
        else:
            if msg == '':
                msg = word
            else:
                msg += ' ' + word
    yield msg


def tweet(api, s):
    for piece in split_long_tweet(s):
        api.update_status(piece)


class GameListener(tweepy.StreamListener):

    def __init__(self, api, game, screen_name):
        self.api = api
        self.game = game
        self.screen_name = screen_name
        self.count = 0

    def handle_command(self, cmd):
        self.game.tell(cmd)
        resp = self.game.listen()
        tweet(self.api, resp)
        self.count += 1
        if (self.count % 15) == 0:
            stats = ('Location: %s, Score: %s, Moves: %s' %
                     (self.game.location, self.game.score, self.game.moves))
            tweet(self.api, stats)

    def on_status(self, status):
        # pprint(status)
        # print("****")
        mentions = status.entities['user_mentions']
        if any(m['screen_name'] == self.screen_name for m in mentions):
            r = re.match('^(\@\S+\s)*(?P<msg>.+)$', status.text)
            if r:
                cmd = r.group('msg')
                print("move is %s" % cmd)
                self.handle_command(cmd)
            else:
                print("ignoring empty reply")

    def on_error(self, status_code):
        if status_code == 420:
            # Disconnect the stream if we get a rate limit error.
            return False


def main(args=sys.argv):
    if len(args) < 2:
        print "usage: <%s> <config file>" % args[0]
    else:
        config = RawConfigParser()
        config.read(args[1])
        screen_name = config.get(config_section, 'screen_name')
        api = get_api(config)
        game = DFrotz(game_file=config.get(config_section, 'game_file'))
        start_message = game.listen()
        tweet(api, start_message)

        listener = GameListener(api, game, screen_name)
        stream = tweepy.Stream(auth=api.auth, listener=listener)
        stream.userstream(_with='user')
