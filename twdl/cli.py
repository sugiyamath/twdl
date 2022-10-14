#!/usr/bin/env python3
import sys
import os
import argparse

from . import run
from . import config
from . import storage


def error(_error, message):
    print("[-] {}: {}".format(_error, message))
    sys.exit(0)


def check(args):
    if args.username is not None and args.userid:
        error("Contradicting Args", "--userid and -u cannot be used together.")
    if args.backoff_exponent <= 0:
        error("Error", "Please specifiy a positive value for backoff_exponent")
    if args.min_wait_time < 0:
        error("Error", "Please specifiy a non negative value for min_wait_time")

def initialize(args):
    c = config.Config()
    c.Username = args.username
    c.User_id = args.userid
    c.Search = args.search
    c.Since = args.since
    c.Until = args.until
    c.Limit = args.limit
    c.Backoff_exponent = args.backoff_exponent
    c.Min_wait_time = args.min_wait_time
    return c


def options():
    ap = argparse.ArgumentParser(prog="twdl", usage="python3 %(prog)s [options]")
    ap.add_argument("-u", "--username", help="User's Tweets you want to scrape.")
    ap.add_argument("-s", "--search", help="Search for Tweets containing this word or phrase.")
    ap.add_argument("--since", help="Filter Tweets sent since date (Example: \"2017-12-27 20:30:15\" or 2017-12-27).", metavar="DATE")
    ap.add_argument("--until", help="Filter Tweets sent until date (Example: \"2017-12-27 20:30:15\" or 2017-12-27).", metavar="DATE")
    ap.add_argument("--userid", help="Twitter user id.")
    ap.add_argument("--limit", help="Number of Tweets to pull (Increments of 20).")
    ap.add_argument("--backoff-exponent", help="Specify a exponent for the polynomial backoff in case of errors.", type=float, default=3.0)
    ap.add_argument("--min-wait-time", type=float, default=15, help="specifiy a minimum wait time in case of scraping limit error. This value will be adjusted by twint if the value provided does not satisfy the limits constraints")
    args = ap.parse_args()
    return args


def main():
    args = options()
    check(args)
    c = initialize(args)
    run.Search(c)


def run_as_command():
    main()


if __name__ == '__main__':
    main()
