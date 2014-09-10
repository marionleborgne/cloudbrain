#!/usr/bin/env python

import json
import os

import socket
import sys
import time
from os.path import dirname, join, realpath


import redis
import msgpack
import random
import math

# Get the current working directory of this file.
# http://stackoverflow.com/a/4060259/120999
__location__ = realpath(join(os.getcwd(), dirname(__file__)))

# Add the shared settings file to namespace.
sys.path.insert(0, join(__location__, '..', 'src'))
import settings


class NoDataException(Exception):
    pass


def seed():
    print 'Loading data over UDP via pipeline...'
    metric = 'channel-%s'
    metric_set = 'unique_metrics'

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  
    end = int(time.time() * 1000) # end in ms
    start = int(end - 5 * 60 * 1000) # 5 last mn

    for k in xrange(7):
        for i in xrange(start, end, 25):
            datapoint = []
            datapoint.append(i)

            value = 50 + math.sin(i*k * 0.001)

            datapoint.append(value)

            metric_name = metric % k
            print (metric_name, datapoint)
            packet = msgpack.packb((metric_name, datapoint))
            sock.sendto(packet, ('localhost', settings.UDP_PORT))
        time.sleep(1)

    print "Connecting to Redis..."
    r = redis.StrictRedis(unix_socket_path=settings.REDIS_SOCKET_PATH)
    time.sleep(5)

    try:
        x = r.smembers(settings.FULL_NAMESPACE + metric_set)
        if x is None:
            raise NoDataException

        x = r.get(settings.FULL_NAMESPACE + metric)
        if x is None:
            raise NoDataException

        #Ignore the mini namespace if OCULUS_HOST isn't set.
        if settings.OCULUS_HOST != "":
            x = r.smembers(settings.MINI_NAMESPACE + metric_set)
            if x is None:
                raise NoDataException

            x = r.get(settings.MINI_NAMESPACE + metric)
            if x is None:
                raise NoDataException

        print "Congratulations! The data made it in. The pipeline pipeline seems to be working."

    except NoDataException:
        print "Woops, looks like the metrics didn't make it into pipeline. Try again?"

if __name__ == "__main__":
    seed()
