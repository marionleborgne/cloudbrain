import pika
import json
import logging
from collections import namedtuple

from cloudbrain.core.config import get_config
from cloudbrain.core.auth import CloudbrainAuth
from cloudbrain.modules.interface import ModuleInterface

_LOGGER = logging.getLogger(__name__)


def _convert_old_chunk_to_new_chunk(old_chunk, num_channels):
    """
    Convert old data chunk to new chunk (i.e. with new data model).
    More on the new data model: https://github.com/NeuroJS/
    eeg-stream-data-model/issues/1#issuecomment-309515243

    :param old_chunk: (list of dict)
        Chunk of data with the old data model
    :param num_channels: (int)
        Number of channels of the input stream.
    :return new_chunk: (dict)
        Chunk of data with the new data model.
    """
    new_chunk = []
    for old_sample in old_chunk:
        num_channels = len(old_sample) - 1  # don't count the 'timestamp' key
        new_sample = {
            'timestamp': old_sample['timestamp'],
            'data': [old_sample['channel_%s' % i] for i in range(num_channels)]
        }
        new_chunk.append(new_sample)

    return {'chunk': new_chunk}


def _get_vhost(username, password):
    config = get_config()
    auth = CloudbrainAuth(config['authUrl'])
    return auth.get_vhost(username, password)


def _setup_mqtt_channel(username, password, host, vhost, exchange):
    credentials = pika.PlainCredentials(username, password)
    params = pika.ConnectionParameters(host=host,
                                       credentials=credentials,
                                       virtual_host=vhost)
    connection = pika.BlockingConnection(parameters=params)
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange, exchange_type='topic',
                             durable=True)
    return channel


MQTTConnection = namedtuple('MQTTConnection',
                            ['host', 'username', 'password', 'vhost',
                             'channel'])


class MQTTConverterSink(ModuleInterface):
    """
    This module subscribes to an AMQP stream, converts it into the
    new data model and publishes it to a MQTT topic with a chosen routing key.
    """

    def __init__(self, subscribers, publishers, mqtt_routing_key):

        super(MQTTConverterSink, self).__init__(subscribers, publishers)
        _LOGGER.debug("Subscribers: %s" % self.subscribers)
        _LOGGER.debug("Publishers: %s" % self.publishers)

        self.routing_key = mqtt_routing_key

        self.exchange = 'amq.topic'  # Default MQTT topic with RabbitMQ
        self.config = get_config()

    def start(self):
        for subscriber in self.subscribers:
            for metric_buffer in subscriber.metric_buffers.values():
                metric_name = metric_buffer.name
                num_channels = metric_buffer.num_channels
                host = subscriber.rabbitmq_address
                username = subscriber.rabbitmq_user
                password = subscriber.rabbitmq_pwd
                vhost = _get_vhost(username, password)
                channel = _setup_mqtt_channel(username, password,
                                              host, vhost, self.exchange)
                mqtt_connection = MQTTConnection(host, username,
                                                 password, vhost, channel)
                callback = self.callback_factory(num_channels, mqtt_connection)
                subscriber.subscribe(metric_name, callback)

    def callback_factory(self, num_channels, mqtt_connection):

        def callback(unused_ch, unused_method, unused_properties, body):
            old_chunk = json.loads(body)
            new_chunk = _convert_old_chunk_to_new_chunk(old_chunk, num_channels)
            mqtt_connection.channel.basic_publish(exchange=self.exchange,
                                                  routing_key=self.routing_key,
                                                  body=json.dumps(new_chunk))

        return callback
