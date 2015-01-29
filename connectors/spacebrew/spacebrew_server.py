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
import argparse

# add the shared settings file to namespace
import sys
from os.path import dirname, abspath

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
import settings

from spacebrew.spacebrew import SpacebrewApp

import logging

logger = logging.getLogger("connectors")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s :: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
handler = logging.FileHandler(settings.LOG_DIR + '/spacebrew_server.log')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger = logging.getLogger("connectors")


class SpacebrewServer(ServerThread):
    def __init__(self, muse_port, muse_id, server):

        self.muse_port = muse_port
        self.muse_id = muse_id

        # Configuring the Muse OSC client
        ServerThread.__init__(self, muse_port)

        logger.info('Muse %s connected to museIO on port %s' % (muse_id, muse_port))

        # configure the Spacebrew client
        self.brew = SpacebrewApp(muse_id, server=server)

        self.osc_paths = [
            '/muse/eeg',
            '/muse/eeg/quantization',
            # '/muse/eeg/dropped_samples',
            '/muse/acc',
            # '/muse/acc/dropped_samples',
            '/muse/batt',
            # '/muse/drlref',
            #'/muse/elements/raw_fft0',
            #'/muse/elements/raw_fft1',
            #'/muse/elements/raw_fft2',
            #'/muse/elements/raw_fft3',
            '/muse/elements/low_freqs_absolute',
            '/muse/elements/delta_absolute',
            '/muse/elements/theta_absolute',
            '/muse/elements/alpha_absolute',
            '/muse/elements/beta_absolute',
            '/muse/elements/gamma_absolute',
            #'/muse/elements/delta_relative',
            #'/muse/elements/theta_relative',
            #'/muse/elements/alpha_relative',
            #'/muse/elements/beta_relative',
            #'/muse/elements/gamma_relative',
            #'/muse/elements/delta_session_score',
            #'/muse/elements/theta_session_score',
            #'/muse/elements/alpha_session_score',
            #'/muse/elements/beta_session_score',
            #'/muse/elements/gamma_session_score',
            '/muse/elements/touching_forehead',
            '/muse/elements/horseshoe',
            '/muse/elements/is_good',
            '/muse/elements/blink',
            '/muse/elements/jaw_clench',
            '/muse/elements/experimental/concentration',
            '/muse/elements/experimental/mellow'
        ]

        for osc_path in self.osc_paths:
            spacebrew_name = self.calculate_spacebrew_name(osc_path)
            self.brew.add_publisher(spacebrew_name, 'string')
            logger.debug('Spacebrew publisher %s added for muse with ID %s' % (spacebrew_name, self.muse_id))

        # Connect to spacebrew
        self.brew.start()

        logger.debug('Initialization completed for muse with ID %s' % self.muse_id)

    def close(self):
        self.brew.stop()
        self.stop()
        logger.info('Connector stopped for muse with ID %s' % self.muse_id)


    # Handle all messages if the OSC path is in self.osc_paths
    @make_method(None, None)
    def fallback(self, path, args, types, src):
        if path in self.osc_paths:
            spacebrew_name = self.calculate_spacebrew_name(path)
            value = ','.join([str(arg) for arg in args])
            self.brew.publish(spacebrew_name, value)
            # logger.debug('Muse with ID %s is publishing to spacebrew. Publisher name: %s. Data: %s' (self.muse_id, spacebrew_name, value))


    def calculate_spacebrew_name(self, osc_path):
        spacebrew_name = osc_path.split('/')[-1]
        return self.disambiguate_name_collisions(spacebrew_name, osc_path)


    def disambiguate_name_collisions(self, spacebrew_name, osc_path):
        if spacebrew_name == 'dropped_samples':
            return osc_path.split('/')[-2] + '_' + osc_path.split('/')[-1]
        else:
            return spacebrew_name


parser = argparse.ArgumentParser(
    description='Send data to Spacebrew.')
parser.add_argument(
    '--name',
    help='Your name or ID without spaces or special characters',
    default='example')
parser.add_argument(
    '--port',
    help='UDP port to accept OSC messages',
    default=5001)
parser.add_argument(
    '--host',
    help='Hostname of Spacebrew server',
    default=settings.EXPLO_BRAINSERVER_IP)

if __name__ == "__main__":
    args = parser.parse_args()
    muse_id = 'muse-%s' % args.name
    server = SpacebrewServer(args.port, muse_id, args.host)
    server.start()
    logger.info('Spacebrew connector stated on port %s for muse with ID %s' % (args.port, muse_id))

