__author__ = 'marion'

# add the shared settings file to namespace
import sys
import argparse
from os.path import dirname, abspath

sys.path.insert(0, dirname(dirname(abspath(__file__))))
import time
from cloudbrain.spacebrew.spacebrew import SpacebrewApp


class SpacebrewClient(object):
    def __init__(self, name, server, paths):
        # configure the spacebrew client
        self.brew = SpacebrewApp(name, server=server)

        for spacebrew_name in paths:
            self.brew.add_subscriber(spacebrew_name, "string")
            self.brew.subscribe(spacebrew_name, self.handle_value)


        self.number_of_packets = 0
        self.start_time = time.time()

    def handle_value(self, value):
        self.number_of_packets += 1
        current_time = time.time()

        if (current_time - self.start_time) % 10 == 0:
            print "current time : %s" %current_time
            print "start time : %s" % self.start_time
            print "==> rate: %" % (self.number_of_packets/(current_time - self.start_time))


    def start(self):
        self.brew.start()



parser = argparse.ArgumentParser(
    description='Output rate of Spacebrew metrics')

parser.add_argument(
    '--name',
    help='Your name or ID without spaces or special characters',
    default='example')

if __name__ == "__main__":

    METRICS = ['mellow', 'concentration']
    SPACEBREW_IP = '104.236.243.233'

    args = parser.parse_args()
    sb_client = SpacebrewClient('rate_meter',  SPACEBREW_IP, METRICS)
    sb_client.start()
