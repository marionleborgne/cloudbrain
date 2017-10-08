import logging
import pika

from cloudbrain.subscribers.interface import SubscriberInterface
from cloudbrain.core.config import get_config
from cloudbrain.core.auth import CloudbrainAuth

_LOGGER = logging.getLogger(__name__)


class PikaSubscriber(SubscriberInterface):
    def __init__(self,
                 base_routing_key,
                 rabbitmq_user,
                 rabbitmq_pwd):

        super(PikaSubscriber, self).__init__(base_routing_key)
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

        queue_name = channel.queue_declare(exclusive=True).method.queue
        channel.queue_bind(exchange=routing_key,
                           queue=queue_name,
                           routing_key=routing_key)

        self.channels[routing_key] = {'channel': channel,
                                      'queue_name': queue_name}

    def disconnect(self):
        for channel in self.channels.values():
            if channel:
                channel['channel'].stop_consuming()
                channel['channel'].close()
        self.connection.close()

    def subscribe(self, metric_name, callback):

        routing_key = '%s:%s' % (self.base_routing_key, metric_name)
        self._rabbitmq_subscribe(routing_key, callback)

    def _rabbitmq_subscribe(self, routing_key, callback):
        channel = self.channels[routing_key]['channel']
        queue_name = self.channels[routing_key]['queue_name']

        channel.basic_consume(callback,
                              queue=queue_name,
                              exclusive=True,
                              no_ack=True)

        channel.start_consuming()

    def get_one_message(self, metric_name):
        routing_key = '%s:%s' % (self.base_routing_key, metric_name)
        return self._rabbitmq_get_one_message(routing_key)

    def _rabbitmq_get_one_message(self, routing_key):
        channel = self.channels[routing_key]['channel']
        queue_name = self.channels[routing_key]['queue_name']
        meth_frame, header_frame, body = channel.basic_get(queue_name)

        return body
