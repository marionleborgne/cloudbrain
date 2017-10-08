import json
import logging
import pika

from cloudbrain.publishers.interface import PublisherInterface
from cloudbrain.core.config import get_config
from cloudbrain.core.auth import CloudbrainAuth

_LOGGER = logging.getLogger(__name__)


class PikaPublisher(PublisherInterface):
    """
    Publish data to RabbitMQ exchanges. The name of the exchange is the
    routing key.
    """

    def __init__(self,
                 base_routing_key,
                 rabbitmq_user,
                 rabbitmq_pwd):

        super(PikaPublisher, self).__init__(base_routing_key)
        _LOGGER.debug("Base routing key: %s" % self.base_routing_key)
        _LOGGER.debug("Routing keys: %s" % self.routing_keys)
        _LOGGER.debug("Metric buffers: %s" % self.metric_buffers)

        self.rabbitmq_user = rabbitmq_user
        self.rabbitmq_pwd = rabbitmq_pwd

        self.connection = None
        self.channels = {}
        self.config = get_config()
        self.rabbitmq_address = self.config['rabbitHost']
        self.auth = CloudbrainAuth(self.config['authUrl'])
        self.rabbitmq_vhost = self.auth.get_vhost(rabbitmq_user, rabbitmq_pwd)

    def connect(self):
        credentials = pika.PlainCredentials(self.rabbitmq_user,
                                            self.rabbitmq_pwd)

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.rabbitmq_address,
            virtual_host=self.rabbitmq_vhost,
            credentials=credentials))

    def disconnect(self):
        for channel in self.channels.values():
            if channel:
                channel.close()
        self.connection.close()

    def register(self, metric_name, num_channels, buffer_size=1):

        routing_key = "%s:%s" % (self.base_routing_key, metric_name)
        self.register_metric(routing_key,
                             metric_name,
                             num_channels,
                             buffer_size)
        self._rabbitmq_register(routing_key)

    def _rabbitmq_register(self, routing_key):
        channel = self.connection.channel()
        channel.exchange_declare(exchange=routing_key, exchange_type='direct')
        self.channels[routing_key] = channel

    def publish(self, metric_name, data):

        routing_key = "%s:%s" % (self.base_routing_key, metric_name)

        # add the data to the metric buffer
        data_to_send = self.metric_buffers[routing_key].add(data)

        # publish only if you reached the max buffer size
        if data_to_send:
            self._rabbitmq_publish(routing_key, data_to_send)

    def _rabbitmq_publish(self, routing_key, data):

        # delivery_mode=2 make the message persistent
        self.channels[routing_key].basic_publish(
            exchange=routing_key,
            routing_key=routing_key,
            body=json.dumps(data),
            properties=pika.BasicProperties(delivery_mode=2))
