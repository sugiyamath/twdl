from datetime import datetime

from . import format, get
from .tweet import Tweet
from .storage import write
import logging as logme

tweets_list = []
author_list = set()


def _formatDateTime(datetimestamp):
    try:
        return int(datetime.strptime(datetimestamp, "%Y-%m-%d %H:%M:%S").timestamp())
    except ValueError:
        return int(datetime.strptime(datetimestamp, "%Y-%m-%d").timestamp())


def clean_lists():
    logme.debug(__name__ + ':clean_lists')
    global tweets_list
    tweets_list = []


def datecheck(datetimestamp, config):
    logme.debug(__name__ + ':datecheck')
    if config.Since:
        logme.debug(__name__ + ':datecheck:SinceTrue')
        d = _formatDateTime(datetimestamp)
        s = _formatDateTime(config.Since)
        if d < s:
            return False
    if config.Until:
        logme.debug(__name__ + ':datecheck:UntilTrue')
        d = _formatDateTime(datetimestamp)
        s = _formatDateTime(config.Until)
        if d > s:
            return False
    logme.debug(__name__ + ':datecheck:dateRangeFalse')
    return True


def is_tweet(tw):
    try:
        tw["data-item-id"]
        logme.debug(__name__ + ':is_tweet:True')
        return True
    except:
        logme.critical(__name__ + ':is_tweet:False')
        return False


def _output(obj, output, config, **extra):
    logme.debug(__name__ + ':_output')
    write.Text(output)
    logme.debug(__name__ + ':_output:Text')


async def checkData(tweet, config):
    logme.debug(__name__ + ':checkData')
    tweet = Tweet(tweet, config)
    if not tweet.datestamp:
        logme.critical(__name__ + ':checkData:hiddenTweetFound')
        print("[x] Hidden tweet found, account suspended due to violation of TOS")
        return
    if datecheck(tweet.datestamp + " " + tweet.timestamp, config):
        output = format.Tweet(config, tweet)
        _output(tweet, output, config)


async def Tweets(tweets, config):
    logme.debug(__name__ + ':Tweets')
    if config.TwitterSearch:
        logme.debug(__name__ + ':Tweets:TwitterSearch')
        await checkData(tweets, config)
    else:
        logme.debug(__name__ + ':Tweets:else')
        if int(tweets["data-user-id"]) == config.User_id:
            await checkData(tweets, config)
