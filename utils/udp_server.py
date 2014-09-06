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
    '--user_name',
    help='The name of the user sending data.',
    default='unknown_user')
parser.add_argument(
    '--mock',
    action='store_true',
    help='Enable mock. Will send mock data without an openBCI board connected.')


class UDPServer(object):

  def __init__(self, ip, port, json, user):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.ip = ip
    self.port = port
    self.json = json
    self.server = socket.socket(
        socket.AF_INET, # Internet
        socket.SOCK_DGRAM)
    self.user = user


  def send_data(self, data):
    self.server.sendto(data, (self.ip, self.port))

  def handle_sample(self, sample):
    print "sample: %s" %sample
    datapoint = sample.channels
    nb_channels = len(datapoint)

    # Just send channel data.
    timestamp = int (time.time())
    for i in xrange(nb_channels):
      metric = "%s.channel-%d" %(self.user, i)
      packet = msgpack.packb((metric, [timestamp, datapoint[i]]))
      self.sock.sendto(packet, ("data.ebrain.io", 8888))
      print "sent packet via UDP for metric %s" % metric


args = parser.parse_args()

sys.path.insert(0, dirname(dirname(abspath(__file__))))
if args.mock:
  import mock_open_bci as open_bci
  print "Mock enabled. Importing 'mock_open_bci' instead of 'open_bci'"
else:
  import open_bci

obci = open_bci.OpenBCIBoard()
if args.filter_data:
  obci.filter_data = True
sock_server = UDPServer(args.host, int(args.port), args.json, args.user_name)
obci.start(sock_server.handle_sample)