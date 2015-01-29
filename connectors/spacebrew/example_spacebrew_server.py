"""
Spacebrew Server with mock data

Note that Spacebrew is required.

Spacebrew installation:
* git clone https://github.com/Spacebrew/spacebrew
* follow the readme instructions to install and start spacebrew
"""

__author__ = 'marion'

# add the shared settings file to namespace
import sys
from os.path import dirname, abspath

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
import settings

import json
from websocket import create_connection
import time
import threading

class SpacebrewServer(object):
    def __init__(self, muse_id=5008, server='127.0.0.1', port=9000):
        self.muse_id = muse_id
        self.server = server
        self.port = port
        self.osc_paths = [
            {'address': "/muse/eeg", 'arguments': 4},
            {'address': "/muse/eeg/quantization", 'arguments': 4},
            {'address': "/muse/eeg/dropped_samples", 'arguments': 1},
            {'address': "/muse/acc", 'arguments': 3},
            {'address': "/muse/acc/dropped_samples", 'arguments': 1},
            {'address': "/muse/batt", 'arguments': 4},
            {'address': "/muse/drlref", 'arguments': 2},
            {'address': "/muse/elements/low_freqs_absolute", 'arguments': 4},
            {'address': "/muse/elements/delta_absolute", 'arguments': 4},
            {'address': "/muse/elements/theta_absolute", 'arguments': 4},
            {'address': "/muse/elements/alpha_absolute", 'arguments': 4},
            {'address': "/muse/elements/beta_absolute", 'arguments': 4},
            {'address': "/muse/elements/gamma_absolute", 'arguments': 4},
            {'address': "/muse/elements/delta_relative", 'arguments': 4},
            {'address': "/muse/elements/theta_relative", 'arguments': 4},
            {'address': "/muse/elements/alpha_relative", 'arguments': 4},
            {'address': "/muse/elements/beta_relative", 'arguments': 4},
            {'address': "/muse/elements/gamma_relative", 'arguments': 4},
            {'address': "/muse/elements/delta_session_score", 'arguments': 4},
            {'address': "/muse/elements/theta_session_score", 'arguments': 4},
            {'address': "/muse/elements/alpha_session_score", 'arguments': 4},
            {'address': "/muse/elements/beta_session_score", 'arguments': 4},
            {'address': "/muse/elements/gamma_session_score", 'arguments': 4},
            {'address': "/muse/elements/touching_forehead", 'arguments': 1},
            {'address': "/muse/elements/horseshoe", 'arguments': 4},
            {'address': "/muse/elements/is_good", 'arguments': 4},
            {'address': "/muse/elements/blink", 'arguments': 1},
            {'address': "/muse/elements/jaw_clench", 'arguments': 1},
            {'address': "/muse/elements/experimental/concentration", 'arguments': 1},
            {'address': "/muse/elements/experimental/mellow", 'arguments': 1}
        ]

        self.ws = create_connection("ws://%s:%s" % (self.server, self.port))


        config = {
            'config': {
                'name': 'muse-%s' % self.muse_id,
                'publish': {
                    'messages': [{'name': name['address'].split('/')[-1], 'type': 'string'} for name in
                                 self.osc_paths]
                }
            }
        }

        self.ws.send(json.dumps(config))

        self.threads = []

    def start(self):
        t = threading.Thread(target=self.send_data)
        self.threads.append(t)
        t.start()

    def send_data(self):
        while 1:
            for path in self.osc_paths:
                spacebrew_name = self.calculate_spacebrew_name(path['address'])
                args = [0.1] * path['arguments']
                value = ','.join([str(arg) for arg in args])

                message = {"message": {
                    "value": value,
                    "type": "string", "name": spacebrew_name, "clientName": 'muse-%s' % self.muse_id}}

                self.ws.send(json.dumps(message))
                time.sleep(0.1)


    def calculate_spacebrew_name(self, osc_path):
        spacebrew_name = osc_path.split('/')[-1]
        return self.disambiguate_name_collisions(spacebrew_name, osc_path)


    def disambiguate_name_collisions(self, spacebrew_name, osc_path):
        if spacebrew_name == 'dropped_samples':
            return osc_path.split('/')[-2] + '_' + osc_path.split('/')[-1]
        else:
            return spacebrew_name


if __name__ == "__main__":

    #muse_ports = settings.MUSE_PORTS
    muse_ports = [7777]
    for muse_port in muse_ports:
        server = SpacebrewServer(muse_id=muse_port, server=settings.EXPLO_BRAINSERVER_IP)
        server.start()
