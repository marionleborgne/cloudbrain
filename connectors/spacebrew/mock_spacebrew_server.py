"""
Spacebrew Server with mock data
To run Spacebrew: cd spacebrew-server & node node_server_forever.js
"""

__author__ = 'marion'

import json
from websocket import create_connection
import time


class SpacebrewServer(object):
    def __init__(self, muse_ids=['muse-001', 'muse-002'], server='127.0.0.1', port=9000):
        self.server = server
        self.port = port
        self.muse_ids = muse_ids
        self.metrics = ['acc', 'eeg', 'mellow', 'concentration']
        self.ws = create_connection("ws://%s:%s" % (self.server, self.port))

        for muse in muse_ids:
            config = {
                'config': {
                    'name': muse,
                    'publish': {
                        'messages': [
                            {
                                'name': 'acc',
                                'type': 'string'
                            },
                            {
                                'name': 'eeg',
                                'type': 'string'
                            },
                            {
                                'name': 'mellow',
                                'type': 'string'
                            },
                            {
                                'name': 'concentration',
                                'type': 'string'
                            }
                        ]
                    }
                }
            }

            self.ws.send(json.dumps(config))

    def start(self):
        while 1:
            for muse_id in self.muse_ids:
                for metric in self.metrics:
                    if metric == 'eeg':
                        value = "[\"/muse/eeg\", 0, 0, 0, 0]"
                    elif metric == 'acc':
                        value = "[\"/muse/acc\", 0, 0, 0]"
                    elif metric == 'concentration':
                        value = "[\"/muse/elements/experimental/concentration\", 0]"
                    elif metric == 'mellow':
                        value = "[\"/muse/elements/experimental/mellow\", 0]"

                    message = {"message": {
                        "value": value,
                        "type": "string", "name": metric, "clientName": muse_id}}
                    self.ws.send(json.dumps(message))
                    time.sleep(0.1)



if __name__ == "__main__":
    server = SpacebrewServer()
    server.start()