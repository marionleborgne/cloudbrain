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
    metric = 'pipeline.test.ebrain.udp'
    metric_set = 'unique_metrics'

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    nbPoints = 300
    end = int(time.time())
    start = int(end - nbPoints)
    anomaly_start_time = (end - 60)
    anomaly_end_time = end


    for i in xrange(start, end):
        datapoint = []
        datapoint.append(i)

        if ((i > anomaly_start_time) and (i < anomaly_end_time)):
            value = int (900 + random.uniform(1,10))
        else:
            value =  int (200 + random.uniform(1,10))

        datapoint.append(value)

        print (metric, datapoint)
        packet = msgpack.packb((metric, datapoint))
        sock.sendto(packet, ('data.ebrain.io', settings.UDP_PORT))


if __name__ == "__main__":
    seed()
