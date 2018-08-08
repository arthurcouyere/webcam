#!/usr/bin/env python

import sys
import ephem
import logging
import argparse

# logging.basicConfig(format='%(asctime)-15s %(message)s')
logging.basicConfig(format='%(message)s')
log = logging.getLogger(__name__)

############################
# check type of light
############################
def type_of_light(latitude, longitude, horizon, event_time=None):

    # location
    o = ephem.Observer()
    o.lat, o.lon, o.horizon = latitude, longitude, horizon
    # o.pressure= 0

    if event_time:
        o.date = event_time

    # get sunrise and sunset time in utc
    previous_sunrise=o.previous_rising (ephem.Sun())
    previous_sunset =o.previous_setting(ephem.Sun())
    log.debug("previous_sunrise=%s" % previous_sunrise)
    log.debug("previous_sunset=%s"  % previous_sunset)
    log.debug("event_date=%s"  % o.date)

    if previous_sunrise > previous_sunset:
        log.debug("type_of_light=day")
        sys.exit(0)
    else:
        log.debug("type_of_light=night")
        sys.exit(1)


############################
# main
############################
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Check if current time is between sunrise and sunset')
    parser.add_argument('-v', action='store_true', help="verbose mode")
    args = parser.parse_args()
    if args.v:
        log.setLevel(logging.DEBUG)


    ret = type_of_light('48.841930', '2.543652', '-0:34')
    if ret == "day":
      sys.exit(0)
    else:
      sys.exit(1)
