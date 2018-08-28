import json
import time
import unittest
from mock import patch

from cloudbrain.modules.sources.openbci import OpenBCISource
from cloudbrain.publishers.rabbitmq import PikaPublisher
from cloudbrain.connectors.openbci import OpenBCIConnector, OpenBCISample



class MockSerial(object):
    """
    Patch class serial.Serial
    """


    def __init__(self, port, baud):
        pass


    def write(self, text):
        pass


    def read(self):
        return 'mock'


    def close(self):
        pass


    def inWaiting(self):
        return False


class MockHTTPResponse(object):

    status_code = 200

    def json(self):
        return {'vhost': 'mock_vhost'}


def mock_requests_get(vhost_info_url, verify):
    return MockHTTPResponse()


def mock_start(self, callback_functions):
    """
    Patch method OpenBCIConnector.start

    :param callback_functions: (dict)
      E.g: {metric_0: callback_0, ...,  metric_N: callback_N}
      where 'metric_X' is a string and 'callback_X' is a function that takes an
      Array as argument.
    """

    packet_id = 0
    channel_data = [i for i in range(8)]
    aux_data = []
    timestamp = int(time.time() * 1000000) # in microseconds
    sample = OpenBCISample(packet_id, channel_data, aux_data, timestamp)
    for (metric, callback_function) in callback_functions.items():
        callback_function(sample)



class MockChannel(object):
    def __init__(self):
        self.published_count = 0
        self.message_published = None


    def exchange_declare(self, exchange, exchange_type):
        pass


    def basic_publish(self, exchange, routing_key, body, properties):
        self.published_count += 1
        self.message_published = body
        print("Message count: %s" % self.published_count)
        print("Message body: %s" % body)



class MockBlockingConnection(object):
    """
    Patch pika's BlockingConnection
    """


    def __init__(self, params):
        pass


    def close(self):
        pass


    def channel(self):
        return MockChannel()



class OpenBCITest(unittest.TestCase):
    def setUp(self):
        self.device = 'openbci'
        self.user = "mock"

        # OpenBCI config
        self.port = None
        self.baud = 0
        self.filter_data = False

        # metric info
        self.metric_name = 'eeg'
        self.num_channels = 8
        self.buffer_size = 2

        # rmq info
        self.rabbitmq_user = 'mock_user'
        self.rabbitmq_pwd = 'mock_pwd'

        self.base_routing_key = '%s:%s' % (self.user, self.device)

        self.message = {'timestamp': 100}
        for i in range(self.num_channels):
            self.message['channel_%s' % i] = i


    def validate_start_method(self, sample):
        self.assertEqual(sample.channel_data, [i for i in range(self.num_channels)])
        print("OpenBCI started: %s" % sample.channel_data)


    @patch('serial.Serial', MockSerial)
    @patch('cloudbrain.connectors.openbci.OpenBCIConnector.start',
           mock_start)
    def test_OpenBCIConnector(self):
        board = OpenBCIConnector()
        callbacks = {self.metric_name: self.validate_start_method}
        board.start(callbacks)


    @patch('requests.get', mock_requests_get)
    @patch('pika.BlockingConnection', MockBlockingConnection)
    def test_PikaPublisher(self):

        options = {"rabbitmq_user": self.rabbitmq_user,
                   "rabbitmq_pwd": self.rabbitmq_pwd}

        publisher = PikaPublisher(self.base_routing_key, **options)
        publisher.connect()
        publisher.register(self.metric_name, self.num_channels,
                           self.buffer_size)

        for metric_name in publisher.metrics_to_num_channels().keys():
            routing_key = "%s:%s" % (self.base_routing_key, metric_name)
            self.assertEqual(publisher.channels[routing_key].published_count, 0)
            self.assertEqual(publisher.channels[routing_key].message_published,
                             None)

            publisher.publish(metric_name, self.message)
            self.assertEqual(publisher.channels[routing_key].published_count, 0)

            publisher.publish(metric_name, self.message)
            self.assertEqual(publisher.channels[routing_key].published_count, 1)

            expected_message = [{
                "channel_5": 5, "channel_4": 4, "channel_7": 7,
                "channel_6": 6, "channel_1": 1, "channel_0": 0,
                "channel_3": 3, "channel_2": 2, "timestamp": 100
            }, {
                "channel_5": 5, "channel_4": 4, "channel_7": 7,
                "channel_6": 6, "channel_1": 1, "channel_0": 0,
                "channel_3": 3, "channel_2": 2, "timestamp": 100
            }]

            published_message = json.loads(
                publisher.channels[routing_key].message_published)
            self.assertEqual(published_message, expected_message)


    @patch('requests.get', mock_requests_get)
    @patch('serial.Serial', MockSerial)
    @patch('pika.BlockingConnection', MockBlockingConnection)
    @patch('cloudbrain.connectors.openbci.OpenBCIConnector.start',
           mock_start)
    def test_OpenBCISource(self):
        options = {"rabbitmq_user": self.rabbitmq_user,
                   "rabbitmq_pwd": self.rabbitmq_pwd}

        publisher = PikaPublisher(self.base_routing_key, **options)
        publisher.connect()
        publisher.register(self.metric_name, self.num_channels,
                           self.buffer_size)

        publishers = [publisher]
        subscribers = []
        source = OpenBCISource(subscribers=subscribers,
                               publishers=publishers,
                               port=self.port,
                               baud=self.baud,
                               filter_data=self.filter_data)
        source.start()

        pub = source.publishers[0]

        routing_key = "%s:%s" % (self.base_routing_key, self.metric_name)
        self.assertEqual(pub.channels[routing_key].published_count, 0)
        self.assertEqual(pub.channels[routing_key].message_published,
                         None, "No messages should have been sent yet.")
