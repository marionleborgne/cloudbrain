# -*- coding: utf-8 -*-

from cloudbrain.settings import RABBITMQ_ADDRESS
from cloudbrain.subscribers.PikaSubscriber import PikaSubscriber

import json

import sockjs.tornado

import tornado.ioloop
import tornado.web


class RtStreamConnection(sockjs.tornado.SockJSConnection):
    """RtStreamConnection connection implementation"""
    # Class level variable
    clients = set()

    def __init__(self, session):
        super(self.__class__, self).__init__(session)
        self.subscriber = None

    def on_open(self, info):
        logging.info("Got a new connection...")
        self.clients.add(self)
        # self.timeout = tornado.ioloop.PeriodicCallback(self.send_heartbeat, 1000)
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

        stream_configuration = json.loads(message)
        device_name = stream_configuration['deviceName']
        device_id = stream_configuration['deviceId']
        metric = stream_configuration['metric']

        if self.subscriber is not None:
            self.subscriber.disconnect()
            self.subscriber = None

        self.subscriber = PikaSubscriber(device_name=device_name,
                                         device_id=device_id,
                                         rabbitmq_address=RABBITMQ_ADDRESS,
                                         metric_name=metric)
        self.subscriber.connect()
        self.subscriber.consume_messages(self.send_probe)

    def on_close(self):
        if self.subscriber is not None:
            self.subscriber.disconnect()
            self.subscriber = None
        # self.timeout.stop()
        self.clients.remove(self)

    def send_probe(self, ch, method, properties, body):
        buffer_content = json.loads(body)
        for record in buffer_content:
            self.send(json.dumps(record.__dict__))

    def send_heartbeat(self):
        self.broadcast(self.clients, 'message')


class MockHandler(tornado.web.RequestHandler):
    """Just a mock page to test it out..."""
    def get(self):
        self.render('mock.html')

if __name__ == "__main__":
    import logging

    logging.getLogger().setLevel(logging.DEBUG)

    # 1. Create chat router
    RtStreamRouter = sockjs.tornado.SockJSRouter(RtStreamConnection, '/rt-stream')

    # 2. Create Tornado application
    app = tornado.web.Application(
            [(r"/", MockHandler)] + RtStreamRouter.urls
    )

    # 3. Make Tornado app listen on Pi
    app.listen(31415)

    # 4. Start IOLoop
    tornado.ioloop.IOLoop.instance().start()
