from async_timeout import timeout
from datetime import datetime
from bs4 import BeautifulSoup
import sys
import socket
import aiohttp
from fake_useragent import UserAgent
import asyncio
import concurrent.futures
import random
from json import loads, dumps
from urllib.parse import quote

from . import url
from .output import Tweets
from .token import TokenExpiryException

import logging as logme

httpproxy = None

user_agent_list = [
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET '
    'CLR 3.5.30729)',
]


def dict_to_url(dct):
    return quote(dumps(dct))


async def RequestUrl(config, init):
    logme.debug(__name__ + ':RequestUrl')
    _serialQuery = ""
    params = []
    _url = ""
    _headers = [("authorization", config.Bearer_token), ("x-guest-token", config.Guest_token)]
    if config.TwitterSearch:
        logme.debug(__name__ + ':RequestUrl:TwitterSearch')
        _url, params, _serialQuery = await url.Search(config, init)        
    response = await Request(_url, params=params, headers=_headers)
    return response


async def Request(_url, params=None, headers=None):
    logme.debug(__name__ + ':Request:Connector')
    async with aiohttp.ClientSession(headers=headers) as session:
        return await Response(session, _url, params)


async def Response(session, _url, params=None):
    logme.debug(__name__ + ':Response')
    with timeout(120):
        async with session.get(_url, ssl=True, params=params) as response:
            resp = await response.text()
            if response.status == 429:  # 429 implies Too many requests i.e. Rate Limit Exceeded
                raise TokenExpiryException(loads(resp)['errors'][0]['message'])
            return resp


async def RandomUserAgent(wa=None):
    logme.debug(__name__ + ':RandomUserAgent')
    try:
        if wa:
            return "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36"
        return UserAgent(verify_ssl=False, use_cache_server=False).random
    except:
        return random.choice(user_agent_list)

async def Tweet(url, config):
    logme.debug(__name__ + ':Tweet')
    try:
        response = await Request(url)
        soup = BeautifulSoup(response, "html.parser")
        tweets = soup.find_all("div", "tweet")
        await Tweets(tweets, config, url)
    except Exception as e:
        logme.critical(__name__ + ':Tweet:' + str(e))


def Limit(Limit, count):
    logme.debug(__name__ + ':Limit')
    if Limit is not None and count >= int(Limit):
        return True


async def Multi(feed, config):
    logme.debug(__name__ + ':Multi')
    count = 0
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            loop = asyncio.get_event_loop()
            futures = []
            for tweet in feed:
                count += 1
                logme.debug(__name__ + ':Multi:else-url')
                link = tweet.find("a", "tweet-timestamp js-permalink js-nav js-tooltip")["href"]
                url = f"https://twitter.com{link}?lang=en"
                logme.debug(__name__ + ':Multi:notUser-full-Run')
                futures.append(loop.run_in_executor(executor, await Tweet(url,
                                                                              config)))
            logme.debug(__name__ + ':Multi:asyncioGather')
            await asyncio.gather(*futures)
    except Exception as e:
        pass
    return count
