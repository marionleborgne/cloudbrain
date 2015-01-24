__author__ = 'marion'

from cassandra.cluster import Cluster

# add the shared settings file to namespace
import sys
from os.path import dirname, abspath

sys.path.insert(0, dirname(dirname(abspath(__file__))))
import settings
from spacebrew.spacebrew import SpacebrewApp

import time

class CassandraSpacebrewClient(object):

    def __init__(self, name, server):
        # configure the spacebrew client
        self.brew = SpacebrewApp(name, server=server)

        self.osc_paths = [
            '/muse/eeg',
            #'/muse/eeg/quantization',
            #'/muse/eeg/dropped_samples',
            #'/muse/acc',
            #'/muse/acc/dropped_samples',
            '/muse/batt',
            #'/muse/drlref',
            #'/muse/elements/raw_fft0',
            #'/muse/elements/raw_fft1',
            #'/muse/elements/raw_fft2',
            #'/muse/elements/raw_fft3',
            #'/muse/elements/low_freqs_absolute',
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

        # configure spacebrew
        for path in self.osc_paths:
            spacebrew_name = self.calculate_spacebrew_name(path)
            self.brew.add_subscriber(spacebrew_name, "string")
            self.brew.subscribe(spacebrew_name, self.handle_value)

        # configure cassandra cluster
        self.cluster = Cluster()
        self.session = self.cluster.connect('cloudbrain')


    def handle_value(self, csv_string):
        args = csv_string.split(',')

        # column family name
        osc_path = args[0]
        column_family_name = self.calculate_spacebrew_name(osc_path)

        # numerical values
        values = args[1:]
        num_arguments = len(values)
        numerical_columns  = ''.join([", value_%s" % i for i in range(num_arguments)])



        # column values
        timestamp = int(time.time() * 1000)
        muse_id = 'muse-5008' # todo: needs to be replaced by real museID
        column_values = "'%s', '%s', %s" % (muse_id, timestamp, values[0])
        if len(values) > 1:
            for value in values[1:]:
                column_values += ", %s" % value


        insert_template = "INSERT INTO %s (muse_id, timestamp%s) VALUES (%s);"
        insert_values = insert_template % (column_family_name, numerical_columns, column_values)

        print insert_values
        self.session.execute(insert_values)


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


if __name__ == "__main__":
    sb_client = CassandraSpacebrewClient('cassandra', settings.CLOUDBRAIN_ADDRESS)
    sb_client.start()
