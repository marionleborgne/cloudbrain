from cloudbrain import settings

__author__ = 'marion'

# add the shared settings file to namespace
import sys
import argparse
from os.path import dirname, abspath

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
from cloudbrain.spacebrew.spacebrew import SpacebrewApp


class SpacebrewClient(object):
    def __init__(self, name, server):
        # configure the spacebrew client
        self.brew = SpacebrewApp(name, server=server)
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

        for path in self.osc_paths:
            spacebrew_name = self.calculate_spacebrew_name(path['address'])
            self.brew.add_subscriber(spacebrew_name, "string")
            self.brew.subscribe(spacebrew_name, self.handle_value)

    def handle_value(self, value):
        print value
        # YOUR CODE HERE


    def start(self):
        self.brew.start()

    def calculate_spacebrew_name(self, osc_path):
        spacebrew_name = osc_path.split('/')[-1]
        return self.disambiguate_name_collisions(spacebrew_name, osc_path)


    def disambiguate_name_collisions(self, spacebrew_name, osc_path):
        if spacebrew_name == 'dropped_samples':
            return osc_path.split('/')[-2] + '_' + osc_path.split('/')[-1]
        else:
            return spacebrew_name


parser = argparse.ArgumentParser(
    description='Receive data from Spacebrew.')
parser.add_argument(
    '--name',
    help='Your name or ID without spaces or special characters',
    default='example')

if __name__ == "__main__":
    args = parser.parse_args()
    sb_client = SpacebrewClient('booth-%s' % args.name, settings.EXPLO_BRAINSERVER_IP)
    sb_client.start()
