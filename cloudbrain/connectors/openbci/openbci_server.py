__author__ = 'marion'

import json
import pika
import sys
import time

import logging
logging.basicConfig()

from openbci_v3 import OpenBCIBoard

_DEVICE_NAME = 'openbci'
_DEVICE_ID = 'openbci_mock'
_HOST = 'localhost'
_EXCHANGE_TYPE = 'direct'


connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=_HOST))
channel = connection.channel()

channel.exchange_declare(exchange=_DEVICE_NAME,
                         type=_EXCHANGE_TYPE)
  
count = 0
messages = []

def handle_sample(sample):
  global messages
  global count
  
  message = {"channel_%s" % i: sample.channel_data[i] for i in xrange(8)}
  message['timestamp'] = int(time.time() * 1000)
  
  if count % 100 == 0:
    channel.basic_publish(exchange=_DEVICE_NAME,
                      routing_key=_DEVICE_ID,
                      body=json.dumps(messages),
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
    messages = [message]
  else:
    messages.append(message)
  
  count += 1
  



board = OpenBCIBoard(port='/dev/tty.OpenBCI-DN0094CZ')

try:
  board.start(handle_sample)
except KeyboardInterrupt:
  connection.close()
  sys.exit()

