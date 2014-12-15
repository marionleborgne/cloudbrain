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

    def __init__(self, port, receiver_ip, receiver_port, user):
        ServerThread.__init__(self, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiver_ip = receiver_ip
        self.receiver_port = receiver_port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.user = user

    # receive accelerometer data
    @make_method('/muse/acc', 'fff')
    def acc_callback(self, path, args):

        data = [path] + args
        self.sock.sendto(json.dumps(data), (self.receiver_ip, self.receiver_port))


    # receive EEG data
    @make_method('/muse/eeg', 'ffff')
    def eeg_callback(self, path, args):
        data = [path] + args
        print data
        self.sock.sendto(json.dumps(data), (self.receiver_ip, self.receiver_port))

    #receive concentration data
    @make_method('/muse/elements/experimental/concentration', 'f')
    def concentration_callback(self, path, args):
        data = [path] + args
        self.sock.sendto(json.dumps(data), (self.receiver_ip, self.receiver_port))


    #receive meditation data
    @make_method('/muse/elements/experimental/mellow', 'f')
    def mellow_callback(self, path, args):
        data = [path] + args
        self.sock.sendto(json.dumps(data), (self.receiver_ip, self.receiver_port))


    #handle unexpected messages
    @make_method(None, None)
    def fallback(self, path, args, types, src):
        # do nothing for now ...
        pass


if __name__ == "__main__":

    try:
        server = MuseServer(9090, 'localhost', 5555, 'marion')
    except ServerError, err:
        print str(err)
        sys.exit()

    try:
        server.start()
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit()