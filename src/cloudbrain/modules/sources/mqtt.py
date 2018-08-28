import json
import logging
import pika
from uuid import uuid4

from cloudbrain.core.config import get_config
from cloudbrain.core.auth import CloudbrainAuth
from cloudbrain.modules.interface import ModuleInterface

_LOGGER = logging.getLogger(__name__)


def _convert_new_chunk_to_old_chunk(new_chunk):
    """
    Convert new chunk (i.e. with new data model) to old chunk.
    More on the new data model: https://github.com/NeuroJS/
    eeg-stream-data-model/issues/1#issuecomment-309515243

    :param new_chunk: (dict)
        Chunk of data with the new data model.
    :return old_chunk: (list of dicts)
       Chunk of data with the old data model
    """
    old_chunk = []
    for sample in new_chunk['chunk']:
        old_sample = {'timestamp': sample['timestamp']}
        for i in range(len(sample['data'])):
            old_sample['channel_%s' % i] = sample['data'][i]
            old_chunk.append(old_sample)
    return old_chunk


def _get_vhost(username, password):
    config = get_config()
    auth = CloudbrainAuth(config['authUrl'])
    return auth.get_vhost(username, password)


def _setup_mqtt_channel(username, password, host, vhost, exchange, routing_key,
                        queue_name):
    credentials = pika.PlainCredentials(username, password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host,
                                  credentials=credentials,
                                  virtual_host=vhost))
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange, exchange_type='topic',
                             durable=True)

    result = channel.queue_declare(queue_name, exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange=exchange,
                       queue=queue_name,
                       routing_key=routing_key)
    return channel


class MQTTConverterSource(ModuleInterface):
    """
    Subscribe to MQTT topic with given routing key, convert data chunks
    from old data model to new, and publish on AMQP exchange.
    """

    def __init__(self,
                 subscribers,
                 publishers,
                 mqtt_routing_key,
                 username,
                 password):

        super(MQTTConverterSource, self).__init__(subscribers, publishers)
        _LOGGER.debug("Subscribers: %s" % self.subscribers)
        _LOGGER.debug("Publishers: %s" % self.publishers)

        self.threads = []
        self.mqtt_routing_key = mqtt_routing_key
        self.username = username
        self.password = password
        self.exchange = 'amq.topic'
        vhost = _get_vhost(username, password)
        host = get_config()['rabbitHost']
        self.queue_name = 'MQTTConverterSource-' + str(uuid4())
        self.mqtt_channel = _setup_mqtt_channel(username, password, host, vhost,
                                                self.exchange, mqtt_routing_key,
                                                self.queue_name)

    def start(self):

        self.mqtt_channel.basic_consume(self.callback,
                                        queue=self.queue_name,
                                        exclusive=True,
                                        no_ack=True)

        self.mqtt_channel.start_consuming()

    def callback(self, ch, method, properties, body):
        new_chunk = json.loads(body)
        old_chunk = _convert_new_chunk_to_old_chunk(new_chunk)

        for publisher in self.publishers:
            for metric_buffer in publisher.metric_buffers.values():
                metric_name = metric_buffer.name
                routing_key = "%s:%s" % (
                publisher.base_routing_key, metric_name)
                publisher._rabbitmq_publish(routing_key, old_chunk)
