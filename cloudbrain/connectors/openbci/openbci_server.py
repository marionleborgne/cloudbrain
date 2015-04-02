__author__ = 'marion'

import socket
import json
import time
  
from openbci_v3 import OpenBCIBoard

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
RCVR_IP = '127.0.0.1'
RCVR_PORT = 5555


def handle_sample(sample):
  timestamp = int(time.time() * 1000)
  packet = json.dumps({'timestamp': timestamp, 'channel_values': sample.channel_data})
  sock.sendto(packet, (RCVR_IP, RCVR_PORT))
  #print(packet)
  

board = OpenBCIBoard(port='/dev/tty.usbserial-DN0094CZ')
board.start(handle_sample)