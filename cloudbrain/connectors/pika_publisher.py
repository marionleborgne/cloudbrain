__author__ = 'marion'

import json
import pika
import sys
import time

import logging

logging.basicConfig()

from publisher import Publisher

_DEVICE_NAME = 'openbci'
_DEVICE_ID = 'openbci_mock'
_HOST = 'localhost'
_EXCHANGE_TYPE = 'direct'


class PikaPublisher(Publisher):
  """
  Publisher implementation for RabbitMQ via the Pika client
  """

  def __init__(self, device_name, device_id, host):
    
    super(PikaPublisher, self).__init__(device_name, device_id, host)
    self.connection = None
    self.channel = None


  def publish(self, buffer_content):
    self.channel.basic_publish(exchange=self.device_name,
                               routing_key=self.device_id,
                               body=json.dumps(buffer_content),
                               properties=pika.BasicProperties(
                                 delivery_mode=2,  # this makes the message persistent
                               ))

  def connect(self):
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(
      host=self.host))
    self.channel = self.connection.channel()

    self.channel.exchange_declare(exchange=self.device_name,
                                  type='direct')

  def disconnect(self):
    self.connection.close()
