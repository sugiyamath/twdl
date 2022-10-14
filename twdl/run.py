import sys, os, datetime
from asyncio import get_event_loop, TimeoutError, ensure_future, new_event_loop, set_event_loop

from . import datelock, feed, get, output, verbose, storage
from .token import TokenExpiryException
from . import token
from .feed import NoMoreTweetsException

import logging as logme

import time

bearer = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs' \
         '%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'


class Twint:
    def __init__(self, config):
        logme.debug(__name__ + ':Twint:__init__')
        self.init = -1
        config.deleted = []
        self.feed: list = [-1]
        self.count = 0
        self.user_agent = ""
        self.config = config
        self.config.Bearer_token = bearer
        self.token = token.Token(config)
        self.token.refresh()
        self.d = datelock.Set(self.config.Until, self.config.Since)


    async def Feed(self):
        logme.debug(__name__ + ':Twint:Feed')
        consecutive_errors_count = 0
        while True:
            try:
                response = await get.RequestUrl(self.config, self.init)
            except TokenExpiryException as e:
                logme.debug(__name__ + 'Twint:Feed:' + str(e))
                self.token.refresh()
                response = await get.RequestUrl(self.config, self.init)

            self.feed = []
            try:
                if self.config.TwitterSearch:
                    try:
                        self.feed, self.init = feed.parse_tweets(self.config, response)
                    except NoMoreTweetsException as e:
                        logme.debug(__name__ + ':Twint:Feed:' + str(e))
                        print('[!] ' + str(e) + ' Scraping will stop now.')
                        print('found {} deleted tweets in this search.'.format(len(self.config.deleted)))
                        break
                break
            except TimeoutError as e:
                logme.critical(__name__ + ':Twint:Feed:' + str(e))
                print(str(e))
                break
            except Exception as e:
                logme.critical(__name__ + ':Twint:Feed:noData' + str(e))
                logme.critical(__name__ + ':Twint:Feed:Tweets_known_error:' + str(e))
                sys.stderr.write(str(e) + " [x] run.Feed")
                sys.stderr.write("[!] if you get this error but you know for sure that more tweets exist, please open an issue and we will investigate it!")
                break

    async def tweets(self):
        await self.Feed()
        logme.debug(__name__ + ':Twint:tweets:notLocation')
        for tweet in self.feed:
            self.count += 1
            await output.Tweets(tweet, self.config)

    async def main(self, callback=None):
        task = ensure_future(self.run())
        if callback:
            task.add_done_callback(callback)
        await task

    async def run(self):
        self.user_agent = await get.RandomUserAgent(wa=True)
        if self.config.User_id is not None and self.config.Username is None:
            logme.debug(__name__ + ':Twint:main:user_id')
            self.config.Username = await get.Username(self.config.User_id, self.config.Bearer_token, self.config.Guest_token)
        if self.config.Username is not None and self.config.User_id is None:
            logme.debug(__name__ + ':Twint:main:username')
            self.config.User_id = await get.User(self.config.Username, self.config, True)
            if self.config.User_id is None:
                raise ValueError("Cannot find twitter account with name = " + self.config.Username)
        if self.config.TwitterSearch and self.config.Since and self.config.Until:
            logme.debug(__name__ + ':Twint:main:search+since+until')
            while self.d.since < self.d.until:
                self.config.Since = datetime.datetime.strftime(self.d.since, "%Y-%m-%d %H:%M:%S")
                self.config.Until = datetime.datetime.strftime(self.d.until, "%Y-%m-%d %H:%M:%S")
                if len(self.feed) > 0:
                    await self.tweets()
                else:
                    logme.debug(__name__ + ':Twint:main:gettingNewTweets')
                    break

                if get.Limit(self.config.Limit, self.count):
                    break
        else:
            logme.debug(__name__ + ':Twint:main:not-search+since+until')
            while True:
                if len(self.feed) > 0:
                    logme.debug(__name__ + ':Twint:main:twitter-search')
                    await self.tweets()
                else:
                    logme.debug(__name__ + ':Twint:main:no-more-tweets')
                    break
                if get.Limit(self.config.Limit, self.count):
                    logme.debug(__name__ + ':Twint:main:reachedLimit')
                    break


def run(config, callback=None):
    logme.debug(__name__ + ':run')
    try:
        get_event_loop()
    except RuntimeError as e:
        if "no current event loop" in str(e):
            set_event_loop(new_event_loop())
        else:
            logme.exception(__name__ + ':run:Unexpected exception while handling an expected RuntimeError.')
            raise
    except Exception as e:
        logme.exception(__name__ + ':run:Unexpected exception occurred while attempting to get or create a new event loop.')
        raise

    get_event_loop().run_until_complete(Twint(config).main(callback))


def Search(config, callback=None):
    logme.debug(__name__ + ':Search')
    config.TwitterSearch = True
    run(config, callback)
