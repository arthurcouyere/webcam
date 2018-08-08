#!/usr/bin/env python

import requests
import dateparser
import datetime
import logging
import argparse

# logging.basicConfig(format='%(asctime)-15s %(message)s')
logging.basicConfig(format='%(message)s')
log = logging.getLogger(__name__)



############################
# get date from http
############################
def get_httpdate(url):

    log.debug("url=%s" % url)
    r = requests.get(url)
    if r.status_code == 200:

        httpdate = r.headers['Date']
        log.debug("httpdate=%s" % httpdate)

        utcdate = dateparser.parse(httpdate)
        log.debug("utcdate=%s" % utcdate)

        localdate = utcdate.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
        log.debug("localdate=%s" % localdate)

        return(localdate)

############################
# main
############################
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='get date and time from http header')
    parser.add_argument('-v', action='store_true', help="verbose mode")
    args = parser.parse_args()
    if args.v:
        log.setLevel(logging.DEBUG)

    httpdate = get_httpdate('http://www.google.com/')
    print(httpdate)

