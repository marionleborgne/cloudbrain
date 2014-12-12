__author__ = 'marion'

from websocket import create_connection
import json
import time


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


    def link(self, metric, muse_id, muse_address, cloudbrain_address):
        message = {
            "route": {
                "type": "add",
                "publisher": {
                    "clientName": muse_id,
                    "name": metric,
                    "type": "string",
                    "remoteAddress": muse_address
                },
                "subscriber": {
                    "clientName": 'cloudbrain',
                    "name": metric,
                    "type": "string",
                    "remoteAddress": cloudbrain_address
                }

            }
        }
        self.ws.send(json.dumps(message))

    def unlink(self, metric, muse_id, muse_address, cloudbrain_address):
        message = {"route":
                       {"type": "remove",
                        "publisher": {
                            "clientName": muse_id,
                            "name": metric,
                            "type": "string",
                            "remoteAddress": muse_address
                        },
                        "subscriber": {
                            "clientName": "cloudbrain",
                            "name": metric,
                            "type": "string",
                            "remoteAddress": cloudbrain_address
                        }},
                   "targetType": "admin"}

        self.ws.send(json.dumps(message))


if __name__ == "__main__":
    router = SpacebrewRouter()
    router.link('eeg', 'muse-001', '127.0.0.1', '127.0.0.1')
    router.link('acc', 'muse-001', '127.0.0.1', '127.0.0.1')
    router.link('concentration', 'muse-001', '127.0.0.1', '127.0.0.1')
    router.link('mellow', 'muse-001', '127.0.0.1', '127.0.0.1')
    time.sleep(1)
    router.unlink("acc", 'muse-001', '127.0.0.1', '127.0.0.1')
