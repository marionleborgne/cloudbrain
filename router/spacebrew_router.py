__author__ = 'marion'

from websocket import create_connection
import json
import time
from pySpacebrew.spacebrew import Spacebrew

# add the shared settings file to namespace
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))
import settings


class SpacebrewRouter(object):
    def __init__(self, server='127.0.0.1', port=9000):
        self.server = server
        self.port = port
        self.ws = create_connection("ws://%s:%s" % (self.server, self.port))

        self.ws.send(json.dumps({"admin": [{"admin": True, "no_msgs": False}]}))

        message = {
            "config": {
                "name": 'router',
                "remoteAddress": self.server
            }
        }

        self.ws.send(json.dumps(message))

        self.brew = Spacebrew("router", description="Spacebrew Router", server=server)

        # Add publishers for RFID connect and disconnect events
        for booth_number in range(1, 24):
            self.brew.addPublisher("booth-{0}-connect".format(booth_number), "string")
            self.brew.addPublisher("booth-{0}-disconnect".format(booth_number), "string")

        self.brew.start()

    def get_spacebrew_config(self):
        message = {
            "status": True
        }
        self.ws.send(json.dumps(message))
        return json.loads(self.ws.recv())

    def link(self, pub_metric, sub_metric, publisher, subscriber, pub_ip, sub_ip):
        message = {
            "route": {
                "type": "add",
                "publisher": {
                    "clientName": publisher,
                    "name": pub_metric,
                    "type": "string",
                    "remoteAddress": pub_ip
                },
                "subscriber": {
                    "clientName": subscriber,
                    "name": sub_metric,
                    "type": "string",
                    "remoteAddress": sub_ip
                }
            }
        }
        self.ws.send(json.dumps(message))
        return json.dumps(message)

    def unlink(self, pub_metric, sub_metric, publisher, subscriber, pub_ip, sub_ip):
        message = {
            "route": {
                "type": "remove",
                "publisher": {
                    "clientName": publisher,
                    "name": pub_metric,
                    "type": "string",
                    "remoteAddress": pub_ip
                },
                "subscriber": {
                    "clientName": subscriber,
                    "name": sub_metric,
                    "type": "string",
                    "remoteAddress": sub_ip
                }
            },
            "targetType": "admin"
        }
        self.ws.send(json.dumps(message))
        return json.dumps(message)

    def connect_event(self, booth, muse):
        self.brew.publish("{0}-connect".format(booth), muse)

    def disconnect_event(self, booth, muse):
        self.brew.publish("{0}-disconnect".format(booth), muse)


if __name__ == "__main__":
    router = SpacebrewRouter(server=settings.CLOUDBRAIN_ADDRESS)
    router.link('eeg', 'eeg', 'muse-001', 'cloudbrain', '127.0.0.1', '127.0.0.1')
    router.link('acc', 'acc', 'muse-001', 'cloudbrain', '127.0.0.1', '127.0.0.1')
    time.sleep(1)
    router.unlink("eeg", 'eeg', 'muse-001', 'cloudbrain', '127.0.0.1', '127.0.0.1')
