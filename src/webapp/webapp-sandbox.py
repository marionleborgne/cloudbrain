import redis
import sys
from os.path import dirname, abspath
from msgpack import Unpacker
import json

# add the shared settings file to namespace
sys.path.insert(0, dirname(dirname(abspath(__file__))))
import settings
import numpy as np
import matplotlib.pyplot as plt


REDIS_CONN = redis.StrictRedis(unix_socket_path=settings.REDIS_SOCKET_PATH)

class Sandbox(object):

    def get_timeserie(self, metric):

        raw_series = REDIS_CONN.get(settings.FULL_NAMESPACE + metric)

        unpacker = Unpacker(use_list = False)
        unpacker.feed(raw_series)
        data = [item[:2] for item in unpacker]

        x = []
        y = []
        for datapoint in data:
            x.append(datapoint[0])
            y.append(datapoint[1])

        timeserie = (x,y)

        return timeserie

    def plot_timeserie(self, timeserie):
        plt.figure()
        plt.plot(timeserie[0], timeserie[1])
        plt.show()




if __name__ == "__main__":

    s = Sandbox()

    metric = "pipeline.test.udp"
    timeserie = s.get_timeserie(metric)
    s.plot_timeserie(timeserie)