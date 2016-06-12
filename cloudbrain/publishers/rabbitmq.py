import json
import logging
import pika

from cloudbrain.publishers.interface import PublisherInterface
from cloudbrain.core.model import MetricBuffer

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)



class PikaPublisher(PublisherInterface):
  """
  RabbitMQ publisher
  """


  def __init__(self, base_routing_key, rabbitmq_address, rabbitmq_user,
               rabbitmq_pwd):

    super(PikaPublisher, self).__init__(base_routing_key)
    logging.debug("Base routing key: %s" % self.base_routing_key)
    logging.debug("Routing keys: %s" % self.routing_keys)
    logging.debug("Metric buffers: %s" % self.metric_buffers)

    self.rabbitmq_address = rabbitmq_address
    self.rabbitmq_user = rabbitmq_user
    self.rabbitmq_pwd = rabbitmq_pwd
    self.connection = None
    self.channels = {}


  def connect(self):
    credentials = pika.PlainCredentials(self.rabbitmq_user, self.rabbitmq_pwd)

    self.connection = pika.BlockingConnection(pika.ConnectionParameters(
      host=self.rabbitmq_address, credentials=credentials))

  def disconnect(self):
    for channel in self.channels.values():
      if channel:
        channel.close()
    self.connection.close()
    

  def register(self, metric_name, num_channels, buffer_size=1):

    routing_key = "%s:%s" % (self.base_routing_key, metric_name)
    if routing_key in self.routing_keys:
      logging.error("Routing key %s already registered. Routing keys: %s" % (
        routing_key, self.routing_keys))
    else:  
      self.routing_keys.append(routing_key)
      channel = self.connection.channel()
      channel.exchange_declare(exchange=routing_key, type='direct')
      self.channels[routing_key] = channel
      self.metric_buffers[routing_key] = MetricBuffer(metric_name, 
                                                      num_channels, buffer_size) 
      logging.info("New routing key registered: %s" % routing_key)
      



  def publish(self, metric_name, data):

    routing_key = "%s:%s" % (self.base_routing_key, metric_name)
    
    # add the data to the metric buffer
    data_to_send = self.metric_buffers[routing_key].add(data)

    # publish only if you reached the max buffer size 
    if data_to_send:
      self.channels[routing_key].basic_publish(exchange=routing_key,
                                               routing_key=routing_key,
                                               body=json.dumps(data_to_send),
                                               properties=pika.BasicProperties(
                                                 delivery_mode=2,
                                                 # makes the message persistent
                                               ))


