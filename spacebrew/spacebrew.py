#!/usr/bin/python
__author__ = 'marion'

import websocket
import threading
import json
import logging
import time


class ConfigurationError(Exception):
    def __init__(self, brew, explanation):
        self.brew = brew
        self.explanation = explanation

    def __str__(self):
        return repr(self.explanation)


class Publisher(object):
    def __init__(self, name, brewType, default=None):
        self.name = name
        self.type = brewType
        self.value = None
        self.default = default

    def make_config(self):
        d = {'name': self.name, 'type': self.type, 'default': self.default}
        return d


class Subscriber(object):
    def __init__(self, name, brewType, default=None):
        self.name = name
        self.type = brewType
        self.value = None
        self.default = default
        self.callbacks = []

    def make_config(self):
        d = {'name': self.name, 'type': self.type, 'default': self.default}
        return d

    def subscribe(self, target):
        self.callbacks.append(target)

    def unsubscribe(self, target):
        self.callbacks.remove(target)

    def disseminate(self, value):
        for target in self.callbacks:
            target(value)


class SpacebrewApp(object):

    def __init__(self, name, description="", server="sandbox.spacebrew.cc", port=9000, admin_app=False):
        self.server = server
        self.port = port
        self.name = name
        self.description = description
        self.connected = False
        self.started = False
        self.publishers = {}
        self.subscribers = {}
        self.ws = None
        self.admin = admin_app

    def add_publisher(self, name, brewType="string", default=None):
        if self.connected:
            raise ConfigurationError(self, "Can not add a new publisher to a running Spacebrew instance (yet).")
        else:
            self.publishers[name] = Publisher(name, brewType, default)

    def add_subscriber(self, name, brewType="string", default=None):
        if self.connected:
            raise ConfigurationError(self, "Can not add a new subscriber to a running Spacebrew instance (yet).")
        else:
            self.subscribers[name] = Subscriber(name, brewType, default)

    def make_config(self):
        subs = map(lambda x: x.make_config(), self.subscribers.values())
        pubs = map(lambda x: x.make_config(), self.publishers.values())
        d = {'config': {
            'name': self.name,
            'description': self.description,
            'publish': {'messages': pubs},
            'subscribe': {'messages': subs},
        }
        }
        return d

    def on_open(self, ws):
        logging.info("Opening brew.")
        if self.admin:
            # register as an admin app
            ws.send(json.dumps({"admin": [{"admin": True, "no_msgs": True}]}))
        ws.send(json.dumps(self.make_config()))
        self.connected = True

    def on_message(self, ws, message):
        msg = json.loads(message)['message']
        sub = self.subscribers[msg['name']]
        sub.disseminate(msg['value'])

    def on_error(self, ws, error):
        logging.error("[on_error] ERROR: {0}".format(error))
        logging.error("[on_error] self started " + str(self.started))
        self.on_close(ws)

    def on_close(self, ws):
        self.connected = False
        while self.started and not self.connected:
            time.sleep(5)
            self.run()

    def publish(self, name, value):
        publisher = self.publishers[name]
        message = {'message': {
            'clientName': self.name,
            'name': publisher.name,
            'type': publisher.type,
            'value': value}}
        self.ws.send(json.dumps(message))


    def subscribe(self, name, target):
        subscriber = self.subscribers[name]
        subscriber.subscribe(target)

    def run(self):
        self.ws = websocket.WebSocketApp("ws://{0}:{1}".format(self.server, self.port),
                                         on_message=lambda ws, msg: self.on_message(ws, msg),
                                         on_error=lambda ws, err: self.on_error(ws, err),
                                         on_close=lambda ws: self.on_close(ws))
        self.ws.on_open = lambda ws: self.on_open(ws)
        self.ws.run_forever()
        self.ws = None

    def start(self):
        self.started = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.started = False
        if self.ws is not None:
            self.ws.close()
        self.thread.join()

