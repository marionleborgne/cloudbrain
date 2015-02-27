"""
Spacebrew Server with mock data

Note that Spacebrew is required.

Spacebrew installation:
* git clone https://github.com/Spacebrew/spacebrew
* follow the readme instructions to install and start spacebrew
"""

__author__ = 'marion'

import time

# add the shared settings file to namespace
import sys
from os.path import dirname, abspath
sys.path.insert(0, (dirname(dirname(abspath(__file__)))))
from cloudbrain.settings import CASSANDRA_METRICS
from cloudbrain.settings import EXPLO_BRAINSERVER_IP

from cloudbrain.spacebrew.spacebrew import SpacebrewApp
from cloudbrain.spacebrew.spacebrew_utils import calculate_spacebrew_name


class SpacebrewServer(object):
    def __init__(self, muse_id=7777, server='127.0.0.1', port=9000):
        self.muse_id = muse_id
        self.server = server
        self.port = port

        name = 'muse-%s' % muse_id
        self.brew = SpacebrewApp(name, server=server)

        for path in CASSANDRA_METRICS:
            publisher_metric_name = calculate_spacebrew_name(path)
            self.brew.add_publisher(publisher_metric_name, "string", '0')
            print publisher_metric_name



    def start(self):
        self.brew.start()
        while 1:
            for path in CASSANDRA_METRICS:

                spacebrew_name = calculate_spacebrew_name(path)
                num_arguments = CASSANDRA_METRICS[path]
                values = [0.1] * num_arguments
                #string value
                value = ','.join([str(v) for v in values])

                self.brew.publish(spacebrew_name, value)
                print spacebrew_name, value
                time.sleep(0.1)

    def stop(self):
        self.brew.stop()


if __name__ == "__main__":

    try:
        server = SpacebrewServer(muse_id=5001, server=EXPLO_BRAINSERVER_IP, port=9000)
        server.start()
    finally:
        server.stop()
