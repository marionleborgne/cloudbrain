# -*- coding: utf-8 -*-

from cloudbrain.settings import RABBITMQ_ADDRESS

import pika
import json
import logging
import argparse

from collections import defaultdict
from sockjs.tornado.conn import SockJSConnection
from sockjs.tornado import SockJSRouter
from tornado.ioloop import PeriodicCallback, IOLoop
from tornado.web import RequestHandler, Application

SERVER_PORT = 31415
logging.getLogger().setLevel(logging.INFO)
recursivedict = lambda: defaultdict(recursivedict)


def get_args_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--cloudbrain', default=RABBITMQ_ADDRESS,
                        help="The address of the RabbitMQ instance you are "
                             "sending data to.\n"
                             "Use %s to send data to our hosted service. \n "
                             "Otherwise use 'localhost' if running CloudBrain "
                             "locally" % RABBITMQ_ADDRESS)
    return parser


def get_opts():
    parser = get_args_parser()
    opts = parser.parse_args()
    return opts


class RtStreamConnection(SockJSConnection):
    """RtStreamConnection connection implementation"""
    # Class level variable
    clients = set()

    def __init__(self, session):
        super(self.__class__, self).__init__(session)
        self.subscribers = recursivedict()


    def send_probe_factory(self, device_id, device_name, metric):

        def send_probe(body):
            logging.debug("GOT: " + body)
            buffer_content = json.loads(body)

            for record in buffer_content:
                record["device_id"] = device_id
                record["device_name"] = device_name
                record["metric"] = metric
                self.send(json.dumps(record))

        return send_probe


    def on_open(self, info):
        logging.info("Got a new connection...")
        self.clients.add(self)
        # self.timeout = PeriodicCallback(self.send_heartbeat, 1000)
        # self.timeout.start()

    # This will receive instructions from the client to change the
    # stream. After the connection is established we expect to receive a JSON
    # with deviceName, deviceId, metric; then we subscribe to RabbitMQ and
    # start streaming the data.
    #
    # NOTE: it's not possible to open multiple connections from the same client.
    #       so in case we need to stream different devices/metrics/etc. at the
    #       same time, we need to use a solution that is like the multiplexing
    #       in the sockjs-tornado examples folder.
    def on_message(self, message):
        logging.info("Got a new message: " + message)

        msg_dict = json.loads(message)
        if msg_dict['type'] == 'subscription':
            self.handle_channel_subscription(msg_dict)
        elif msg_dict['type'] == 'unsubscription':
            self.handle_channel_unsubscription(msg_dict)

    def handle_channel_subscription(self, stream_configuration):
        device_name = stream_configuration['deviceName']
        device_id = stream_configuration['deviceId']
        metric = stream_configuration['metric']

        if not self.metric_exists(device_id, device_name, metric):
            self.subscribers[device_id][device_name][metric] = TornadoSubscriber(
                callback=self.send_probe_factory(device_id, device_name, metric),
                device_name=device_name,
                device_id=device_id,
                rabbitmq_address=RABBITMQ_ADDRESS,
                metric_name=metric)

            self.subscribers[device_id][device_name][metric].connect()

    def handle_channel_unsubscription(self, unsubscription_msg):
        device_name = unsubscription_msg['deviceName']
        device_id = unsubscription_msg['deviceId']
        metric = unsubscription_msg['metric']

        logging.info("Unsubscription received for device_id: %s, device_name: %s, metric: %s"
                     % (device_id, device_name, metric))
        if self.metric_exists(device_id, device_name, metric):
            self.subscribers[device_id][device_name][metric].disconnect()

    def on_close(self):
        logging.info("Disconnecting client...")
        for device_id in self.subscribers:
            for device_name in self.subscribers[device_id]:
                for metric in self.subscribers[device_id][device_name]:
                    subscriber = self.subscribers[device_id][device_name][metric]
                    if subscriber is not None:
                        logging.info("Disconnecting subscriber for device_id: %s, device_name: %s, metric: %s"
                                     % (device_id, device_name, metric))
                        subscriber.disconnect()

        self.subscribers = {}
        #self.timeout.stop()
        self.clients.remove(self)
        logging.info("Client disconnection complete!")

    def send_heartbeat(self):
        self.broadcast(self.clients, 'message')

    def metric_exists(self, device_id, device_name, metric):
        return (self.subscribers.has_key(device_id)
                and self.subscribers[device_id].has_key(device_name)
                and self.subscribers[device_id][device_name].has_key(metric))

class MockHandler(RequestHandler):
    """Just a mock page to test it out..."""
    def get(self):
        self.render('mock.html')


class RtDataStreamHandler(RequestHandler):
    """
    Just a custom handler for the rt-data-stream.js file :)
    """
    def get(self):
        self.render('rt-data-stream.js')


# See: https://pika.readthedocs.org/en/0.9.14/examples/tornado_consumer.html
class TornadoSubscriber(object):

    def __init__(self, callback, device_name, device_id,
                 rabbitmq_address, metric_name):
        self.callback = callback
        self.device_name = device_name
        self.device_id = device_id
        self.metric_name = metric_name

        self.connection = None
        self.channel = None

        self.host = RABBITMQ_ADDRESS
        self.queue_name = None


    def connect(self):
        credentials = pika.PlainCredentials('cloudbrain', 'cloudbrain')
        self.connection = pika.adapters.tornado_connection.TornadoConnection(
            pika.ConnectionParameters(
                host=self.host, credentials=credentials),
            self.on_connected,
            stop_ioloop_on_close=False,
            custom_ioloop=IOLoop.instance())

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def on_connected(self, connection):
        self.connection = connection
        self.connection.add_on_close_callback(self.on_connection_closed)
        self.connection.add_backpressure_callback(self.on_backpressure_callback)
        self.open_channel()

    def on_connection_closed(self, connection, reply_code, reply_text):
        self.connection = None
        self.channel = None

    def on_backpressure_callback(self, connection):
        logging.info("******** Backpressure detected for %s" % self.get_key())

    def open_channel(self):
        self.connection.channel(self.on_channel_open)

    def on_channel_open(self, channel):
        self.channel = channel
        self.channel.add_on_close_callback(self.on_channel_closed)
        # self.setup_exchange(self.EXCHANGE)
        # self.channel.confirm_delivery(self.on_delivery_confirmation)
        logging.info("Declaring exchange: %s" % self.get_key())
        self.channel.exchange_declare(self.on_exchange_declareok,
                                      exchange=self.get_key(),
                                      type='direct',
                                      passive=True)

    def on_channel_closed(self, channel, reply_code, reply_text):
        self.connection.close()

    def on_exchange_declareok(self, unused_frame):
        self.channel.queue_declare(self.on_queue_declareok,
                                   self.get_key(),
                                   exclusive=True,)

    def on_queue_declareok(self, unused_frame):
        logging.info("Binding queue: " + self.get_key())
        self.channel.queue_bind(
                       self.on_bindok,
                       exchange=self.get_key(),
                       queue=self.get_key(),
                       routing_key=self.get_key())

    def on_bindok(self, unused_frame):
        self.channel.add_on_cancel_callback(self.on_consumer_cancelled)
        self.consumer_tag = self.channel.basic_consume(self.on_message,
                                                       self.get_key(),
                                                       exclusive=True,
                                                       no_ack=True)

    def on_consumer_cancelled(self, method_frame):
        if self.channel:
            self.channel.close()

    def on_message(self, unused_channel, basic_deliver, properties, body):
        self.acknowledge_message(basic_deliver.delivery_tag)
        self.callback(body)

    def acknowledge_message(self, delivery_tag):
        self.channel.basic_ack(delivery_tag)

    def get_key(self):
        key = "%s:%s:%s" %(self.device_id,self.device_name, self.metric_name)
        return key

if __name__ == "__main__":

    # 0. Toggle localhost if you want
    opts = get_opts()
    RABBITMQ_ADDRESS = opts.cloudbrain

    # 1. Create chat router
    RtStreamRouter = SockJSRouter(RtStreamConnection, '/rt-stream')

    # 2. Create Tornado application
    app = Application(
        [(r"/", MockHandler),
         (r"/rt-data-stream.js", RtDataStreamHandler)] + RtStreamRouter.urls)

    # 3. Make Tornado app listen on Pi
    app.listen(SERVER_PORT)

    print "Real-time data server running at http://localhost:%s" % SERVER_PORT

    # 4. Start IOLoop
    IOLoop.instance().start()
