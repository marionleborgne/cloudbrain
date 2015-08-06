#!/usr/bin/env python
import pika
from subscriber import Subscriber


_DEVICE_ID = "my_device"
_DEVICE_NAME = "muse"
_HOST = "localhost"
_BUFFER_SIZE = 100

class PikaSubscriber(Subscriber):
  
  def __init__(self, device_name, device_id, host):
    super(PikaSubscriber, self).__init__(device_name, device_id, host)
    self.connection = None
    self.channel = None
    self.queue_name = None
    
    
  def connect(self):
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(
      host=self.host))
    self.channel = self.connection.channel()

    self.channel.exchange_declare(exchange=self.device_name,
                                  type='direct')

    self.queue_name = self.channel.queue_declare(exclusive=True).method.queue
    
    
    self.channel.queue_bind(exchange=self.device_name,
                   queue=self.queue_name,
                   routing_key=self.device_id)

  def disconnect(self):
    self.connection.close()
    
    
  def consume_messages(self, callback):
    self.channel.basic_consume(callback,
                      queue=self.queue_name,
                      exclusive=True,
                      no_ack=True)

    self.channel.start_consuming()
    

  def get_one_message(self):
    for method, properties, body in self.channel.consume(self.queue_name, exclusive=True, no_ack=True):
      return body

def _print_message(ch, method, properties, body):
  print body

    
if __name__ == "__main__":
  subscriber = PikaSubscriber(_DEVICE_NAME, _DEVICE_ID, _HOST)
  subscriber.connect()
  #subscriber.consume_messages(_print_message)
  print subscriber.get_one_message()




