"""
Muse Server.

To start MuseIO, open a terminal or command prompt and type:

muse-io --osc osc.udp://localhost:5001,osc.udp://localhost:5002

"""

__author__ = 'marion'

from liblo import ServerThread, ServerError, make_method
import sys
import time
import socket
import json

from sandbox.muse.cassandra_settings import BATCH_MAX_SIZE


MUSE_ACC = '/muse/acc'
MUSE_EEG = '/muse/eeg'

class MuseServer(ServerThread):
    def __init__(self, sender_ip, sender_port, receiver_ip, receiver_port, user):
        # listen for messages on port 5001
        ServerThread.__init__(self, 5001)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sender_ip = sender_ip
        self.receiver_ip = receiver_ip
        self.receiver_port = receiver_port
        self.sender_port = sender_port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.user = user
        self.metrics = [MUSE_ACC, MUSE_EEG]
        self.batches = {}  # keep track of the batches of data being sent
        for metric in self.metrics:  # initialize all batches
            self.batches[metric] = {}
        self.start_time = int(time.time() * 1000)

    # receive accelerometer data
    @make_method(MUSE_ACC, 'fff')
    def acc_callback(self, path, args):

        # data
        acc_x, acc_y, acc_z = args

        # create batch
        timestamp = int(time.time() * 1000)
        row_key = str(timestamp)
        column = {'path': path,
                  'acc_x': str(acc_x),
                  'acc_y': str(acc_y),
                  'acc_z': str(acc_z),
                  'timestamp': str(timestamp)}
        self.batches[MUSE_ACC][row_key] = column

        # if the batch is big enough, send it
        if len(self.batches[MUSE_ACC]) == BATCH_MAX_SIZE:
            # send batch
            self.sock.sendto(json.dumps(self.batches[MUSE_ACC]), (self.receiver_ip, self.receiver_port))

            # performance stats
            time_to_create_batch = int(time.time() * 1000) - self.start_time
            print 'time to create batch (%s points): %s ms -- %s ms per point' % (len(self.batches[MUSE_ACC]),
                                                                                  time_to_create_batch,
                                                                                  time_to_create_batch /
                                                                                  len(self.batches[MUSE_ACC]))
            self.start_time = int(time.time() * 1000)

            # reset batch after sending it
            self.batches[MUSE_ACC] = {}


    # receive EEG data
    @make_method('/muse/eeg', 'ffff')
    def eeg_callback(self, path, args):
        l_ear, l_forehead, r_forehead, r_ear = args
        timestamp = int(time.time() * 1000)
        packet = json.dumps({'path': path,
                             'l_ear': l_ear,
                             'l_forehead': l_forehead,
                             'r_forehead': r_forehead,
                             'r_ear': r_ear,
                             'timestamp': timestamp})
        #self.sock.sendto(packet, (self.receiver_ip, self.receiver_port))

    #receive concentration data
    @make_method('/muse/elements/experimental/concentration', 'f')
    def concentration_callback(self, path, args):
        concentration = args[0]
        timestamp = int(time.time() * 1000)
        packet = json.dumps({'path': path,
                             'concentration': concentration,
                             'timestamp': timestamp})
        #self.sock.sendto(packet, (self.receiver_ip, self.receiver_port))


    #receive meditation data
    @make_method('/muse/elements/experimental/mellow', 'f')
    def mellow_callback(self, path, args):
        mellow = args[0]
        timestamp = int(time.time() * 1000)
        packet = json.dumps({'path': path,
                             'mellow': mellow,
                             'timestamp': timestamp})
        #self.sock.sendto(packet, (self.receiver_ip, self.receiver_port))


    #handle unexpected messages
    @make_method(None, None)
    def fallback(self, path, args, types, src):
        # do nothing for now ...
        pass


if __name__ == "__main__":

    try:
        server = MuseServer('localhost', 8888, 'localhost', 5555, 'marion')
    except ServerError, err:
        print str(err)
        sys.exit()

    server.start()

    while 1:
        time.sleep(1)