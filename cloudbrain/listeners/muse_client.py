"""
Client for the Muse server.
"""

__author__ = 'marion'

import json
import sys
import socket


class MuseClient(object):
    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.bind((ip, port))

    def listen(self):

        while 1:
            data = self.client.recv(1024)
            value = json.loads(data)
            print value


if __name__ == "__main__":
    muse_client = MuseClient('localhost', 5555)
    try:
        muse_client.listen()
    except KeyboardInterrupt:
        sys.exit()
