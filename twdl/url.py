import datetime
from sys import platform
import logging as logme
from urllib.parse import urlencode
from urllib.parse import quote

mobile = "https://mobile.twitter.com"
base = "https://api.twitter.com/2/search/adaptive.json"


def _sanitizeQuery(_url, params):
    _serialQuery = ""
    _serialQuery = urlencode(params, quote_via=quote)
    _serialQuery = _url + "?" + _serialQuery
    return _serialQuery


def _formatDate(date):
    if "win" in platform:
        return f'\"{date.split()[0]}\"'
    try:
        return int(datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").timestamp())
    except ValueError:
        return int(datetime.datetime.strptime(date, "%Y-%m-%d").timestamp())


async def Search(config, init):
    logme.debug(__name__ + ':Search')
    url = base
    tweet_count = 100
    q = ""
    params = [
        # ('include_blocking', '1'),
        # ('include_blocked_by', '1'),
        # ('include_followed_by', '1'),
        # ('include_want_retweets', '1'),
        # ('include_mute_edge', '1'),
        # ('include_can_dm', '1'),
        ('include_can_media_tag', '1'),
        # ('skip_status', '1'),
        # ('include_cards', '1'),
        ('include_ext_alt_text', 'true'),
        ('include_quote_count', 'true'),
        ('include_reply_count', '1'),
        ('tweet_mode', 'extended'),
        ('include_entities', 'true'),
        ('include_user_entities', 'true'),
        ('include_ext_media_availability', 'true'),
        ('send_error_codes', 'true'),
        ('simple_quoted_tweet', 'true'),
        ('count', tweet_count),
        ('query_source', 'typed_query'),
        # ('pc', '1'),
        ('cursor', str(init)),
        ('spelling_corrections', '1'),
        ('ext', 'mediaStats%2ChighlightedLabel'),
        ('tweet_search_mode', 'live'),  # this can be handled better, maybe take an argument and set it then
    ]

    params.append(('f', 'tweets'))
    if config.Query:
        q += f" from:{config.Query}"
    if config.Username:
        q += f" from:{config.Username}"
    if config.Search:
        q += f" {config.Search}"
    if config.Since:
        q += f" since:{_formatDate(config.Since)}"
    if config.Until:
        q += f" until:{_formatDate(config.Until)}"
    q = q.strip()
    params.append(("q", q))
    _serialQuery = _sanitizeQuery(url, params)
    return url, params, _serialQuery
