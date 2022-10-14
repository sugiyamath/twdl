
import logging as logme

def Tweet(config, t):
    logme.debug(__name__+':Tweet:notFormat')
    output = f"{t.id_str} {t.datestamp} {t.timestamp} {t.timezone} <{t.username}> {t.tweet} [:::]"
    output += f"{t.replies_count}::{t.retweets_count}::{t.likes_count}[:::]"
    return output
