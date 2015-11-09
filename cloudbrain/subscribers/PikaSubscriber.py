import pika
import json
from cloudbrain.subscribers.SubscriberInterface import Subscriber
from cloudbrain.utils.metadata_info import get_metrics_names
from cloudbrain.settings import RABBITMQ_ADDRESS


class PikaSubscriber(Subscriber):

  def __init__(self, device_name, device_id, rabbitmq_address, metric_name):
    super(PikaSubscriber, self).__init__(device_name, device_id, rabbitmq_address)
    self.connection = None
    self.channel = None
    self.queue_name = None
    self.metric_name = metric_name


  def connect(self):
    credentials = pika.PlainCredentials('cloudbrain', 'cloudbrain')
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(
      host=self.host, credentials=credentials))
    self.channel = self.connection.channel()

    key = "%s:%s:%s" %(self.device_id,self.device_name, self.metric_name)
    self.channel.exchange_declare(exchange=key,
                                  type='direct')

    self.queue_name = self.channel.queue_declare(exclusive=True).method.queue


    self.channel.queue_bind(exchange=key,
                   queue=self.queue_name,
                   routing_key=key)

  def disconnect(self):
    self.connection.close_file()


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

  device_id = "test"
  device_name = "muse"
  host = RABBITMQ_ADDRESS
  buffer_size = 100

  metric_names = get_metrics_names(device_name)

  while 1:
    for metric in metric_names:
      print metric
      subscriber = PikaSubscriber(device_name, device_id, host, metric)
      subscriber.connect()
      #subscriber.consume_messages(_print_message)
      buffer = json.loads(subscriber.get_one_message())
      for record in buffer:
        print record
