"""
Muse Server.

Note that both Spacebrew and the MuseIO SDK are required

Spacebrew installation:
* git clone https://github.com/Spacebrew/spacebrew
* follow the readme instructions to install and start spacebrew

To start MuseIO, open a terminal or command prompt and type:

muse-io --osc osc.udp://localhost:9090

"""

__author__ = 'marion'

from liblo import ServerThread, make_method
import json
import argparse

# add the shared settings file to namespace
import sys
from os.path import dirname, abspath

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
import settings

from spacebrew.spacebrew import SpacebrewApp


class SpacebrewServer(ServerThread):
    def __init__(self, muse_port, muse_id, server):
        # Configuring the Muse OSC client
        ServerThread.__init__(self, muse_port)

        # configure the Spacebrew client
        self.brew = SpacebrewApp(muse_id, server=server)

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

        self.paths = [path['address'] for path in self.osc_paths]

        for path in self.paths:
            spacebrew_name = path.split('/')[-1]
            self.brew.add_publisher(spacebrew_name, "string")

        # connect to spacebrew
        self.brew.start()


    def close(self):
        self.brew.stop()
        self.stop()


    # handle all messages if the OSC path is in self.paths
    @make_method(None, None)
    def fallback(self, path, args, types, src):

        if path in self.paths:
            data = [path] + args

            sb_name = path.split('/')[-1]
            self.brew.publish(sb_name, json.dumps(data))


parser = argparse.ArgumentParser(
    description='Send data to Spacebrew.')
parser.add_argument(
    '--name',
    help='Your name or ID without spaces or special characters',
    default='example')

if __name__ == "__main__":
    args = parser.parse_args()
    server = SpacebrewServer(9090, 'muse-%s' % args.name, settings.CLOUDBRAIN_ADDRESS)
    server.start()


