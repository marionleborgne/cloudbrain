__author__ = 'marion'
import requests
import json
import msgpack
import socket
import sys
from os.path import dirname, abspath
import redis
import time
import random
import matplotlib.pyplot as plt
import numpy as np

# add the shared settings file to namespace
sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
import settings


class NoDataException(Exception):
    pass

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_host = "localhost"
metric_set = 'unique_metrics'

# signal timescales
full_duration = 3600
end = int(time.time())
start = end - full_duration
anomaly_duration = 30
anomaly_start = end - anomaly_duration
anomaly_end = end
timestamps = xrange(start, end)

# steady function
metric = "steady_function"
steady_values = []
signal_value = 10
for timestamp in timestamps:
    value = random.random() + signal_value
    if anomaly_start < timestamp < anomaly_end:
        value *= 2
    point = [timestamp, value]
    steady_values.append(value)
    packet = msgpack.packb((metric, point))
    sock.sendto(packet, (socket_host, settings.UDP_PORT))

# step function
metric = "step_function"
step_values = []
signal_value = 10
signal_period = 300
level = 1
for timestamp in timestamps:
    if timestamp % signal_period == 0:
        level *= -1
    if level == 1:
        level_value = signal_value
    elif level == -1:
        level_value = 0
    value = random.random() + level_value
    if anomaly_start < timestamp < anomaly_end:
        value *= 3
    point = [timestamp, value]
    step_values.append(value)
    packet = msgpack.packb((metric, point))
    sock.sendto(packet, (socket_host, settings.UDP_PORT))

# triangular function
metric = "triangular_function"
trig_values = []
signal_value = 100
signal_period = 100
level = -1
level_value = signal_value
for timestamp in timestamps:
    if timestamp % signal_period == 0:
        level *= -1

    if level == 1:
        level_value += 0.7
    elif level == -1:
        level_value -= 0.7
    value = random.random()*10 + level_value
    if anomaly_start < timestamp < anomaly_end:
        value *= 2
    point = [timestamp, value]
    trig_values.append(value)
    packet = msgpack.packb((metric, point))
    sock.sendto(packet, (socket_host, settings.UDP_PORT))

'''
# plot template functions
plt.figure()
plt.plot(timestamps, step_values, label=metric)
plt.plot(timestamps, steady_values, label=metric)
plt.plot(timestamps, trig_values, label=metric)
plt.show()
'''

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

    print "Congratulations! The data made it in. The pipeline pipeline seems to be working."

except NoDataException:
    print "Woops, looks like the metrics didn't make it into pipeline. Try again?"


