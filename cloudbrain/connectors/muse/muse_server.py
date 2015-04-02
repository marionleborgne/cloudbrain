"""
Muse Server.

To start MuseIO, open a terminal or command prompt and type:

muse-io --osc osc.udp://localhost:9090

"""

__author__ = 'marion'

from liblo import ServerThread, ServerError, make_method
import sys
import time
import socket
import json


class MuseServer(ServerThread):

    def __init__(self, muse_port, client_ip, client_port):
        ServerThread.__init__(self, muse_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_ip = client_ip
        self.client_port = client_port


    # receive EEG data
    @make_method('/muse/eeg', 'ffff')
    def eeg_callback(self, path, args):
        self.sock.sendto(json.dumps(args), (self.client_ip, self.client_port))
        print path, args


    # receive horseshoe data
    @make_method("/muse/elements/horseshoe", 'ffff')
    def horseshoe_callback(self, path, args):
        pass  # do nothing for now
        print path, args


    #receive concentration data
    @make_method('/muse/elements/experimental/concentration', 'f')
    def concentration_callback(self, path, args):
        pass  # do nothing for now
        #print path, args

    #receive meditation data
    @make_method('/muse/elements/experimental/mellow', 'f')
    def mellow_callback(self, path, args):
        pass  # do nothing for now
        #print path, args


    #handle unexpected messages
    @make_method(None, None)
    def fallback(self, path, args, types, src):
        pass  # do nothing for now
        #print path, args



if __name__ == "__main__":

    try:
        server = MuseServer(9090, 'localhost', 5555)
    except ServerError, err:
        print str(err)
        sys.exit()

    try:
        server.start()
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit()