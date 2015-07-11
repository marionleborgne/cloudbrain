__author__ = 'marion'

import json
import pika
import sys
import time

import logging
logging.basicConfig()

from openbci_v3 import OpenBCIBoard

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='openbci', durable=True)
  
count = 0
messages = []

def handle_sample(sample):
  global messages
  global count
  
  message = {"channel_%s" % i: sample.channel_data[i] for i in xrange(8)}
  message['timestamp'] = int(time.time() * 1000)
  
  if count % 100 == 0:
    channel.basic_publish(exchange='openbci',
                      routing_key='openbci',
                      body=json.dumps(messages),
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
    messages = [message]
  else:
    messages.append(message)
  
  count += 1
  

  '''
  
  channel.basic_publish(exchange='openbci',
                      routing_key='openbci',
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
                      
  '''


board = OpenBCIBoard(port='/dev/tty.usbserial-DN0094CZ')

try:
  board.start(handle_sample)
except KeyboardInterrupt:
  connection.close()
  sys.exit()

