#!/usr/bin/env python

import json
import os
import math
import socket
import sys
import time
from os.path import dirname, join, realpath


import redis
import msgpack
import random

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

    nbPoints = 84600
    end = int(time.time() * 1000)
    start = int(end - nbPoints)

    for k in xrange(7):
        for i in xrange(start, end):
            datapoint = []
            datapoint.append(i)

            value = 50 + math.sin(i*k * 0.001)

            datapoint.append(value)

            metric_name = metric % k
            print (metric_name, datapoint)
            packet = msgpack.packb((metric_name, datapoint))
            sock.sendto(packet, ('data.ebrain.io', settings.UDP_PORT))
        time.sleep(1)



if __name__ == "__main__":
    seed()
