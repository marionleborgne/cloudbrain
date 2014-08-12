"""A server that handles a connection with an OpenBCI board and serves that
data over both a UDP socket server and a WebSocket server.

Requires:
  - pyserial
  - asyncio
  - websockets
"""

import argparse
import cPickle as pickle
import socket
import time

import msgpack
import sys
from os.path import dirname, abspath

sys.path.insert(0, dirname(dirname(abspath(__file__))))
import open_bci


parser = argparse.ArgumentParser(
    description='Run a UDP server streaming OpenBCI data.')
parser.add_argument(
    '--json',
    action='store_true',
    help='Send JSON data rather than pickled Python objects.')
parser.add_argument(
    '--filter_data',
    action='store_true',
    help='Enable onboard filtering.')
parser.add_argument(
    '--host',
    help='The host to listen on.',
    default='127.0.0.1')
parser.add_argument(
    '--port',
    help='The port to listen on.',
    default='8888')
parser.add_argument(
    '--serial',
    help='The serial port to communicate with the OpenBCI board.',
    default='/dev/tty.usbmodem1411')
parser.add_argument(
    '--baud',
    help='The baud of the serial connection with the OpenBCI board.',
    default='115200')


class UDPServer(object):

  def __init__(self, ip, port, json):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.ip = ip
    self.port = port
    self.json = json
    self.server = socket.socket(
        socket.AF_INET, # Internet
        socket.SOCK_DGRAM)



  def send_data(self, data):
    self.server.sendto(data, (self.ip, self.port))

  def handle_sample(self, sample):
    datapoint = sample.channels
    nb_channels = len(datapoint)

    if True:
      # Just send channel data.
      timestamp = int (time.time())
      for i in xrange(nb_channels):
        metric = "channel-%d" %i
        packet = msgpack.packb((metric, [timestamp, datapoint[i]]))
        #self.send_data(packet)
        self.sock.sendto(packet, ("localhost", 8888))
        print "sent packet via UDP for metric %s" % metric

    else:
      # Pack up and send the whole OpenBCISample object.
      self.send_data(pickle.dumps(sample))


args = parser.parse_args()
obci = open_bci.OpenBCIBoard(args.serial, int(args.baud))
if args.filter_data:
  obci.filter_data = True
sock_server = UDPServer(args.host, int(args.port), args.json)
obci.start(sock_server.handle_sample)