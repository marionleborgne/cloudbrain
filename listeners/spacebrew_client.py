__author__ = 'marion'

# add the shared settings file to namespace
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))
import settings

from spacebrew.spacebrew import SpacebrewApp
from database.old.cassandra_repository import CassandraRepository
from database.old.cassandra_repository import convert_muse_data_to_cassandra_column
from database.old.cassandra_settings import KEYSPACE
from database.old.cassandra_settings import MUSE_COLUMN_FAMILY
from database.old.cassandra_settings import BATCH_MAX_SIZE


class SpacebrewClient(object):

    def __init__(self, name, server):
        # get app name and server from query string
        self.name = name
        server = server

        # configure the spacebrew client
        self.brew = SpacebrewApp(name, server=server)

        # cassandra
        self.muse_cassandra_repo = CassandraRepository(KEYSPACE, MUSE_COLUMN_FAMILY)
        self.batches = {}
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
            spacebrew_name = path['address'].split('/')[-1]
            self.brew.add_subscriber(spacebrew_name, "string")
            self.brew.subscribe(spacebrew_name, self.handle_value)

    def handle_value(self, value):
        path = value[0]
        if path in self.paths:
            row_key, column = convert_muse_data_to_cassandra_column(path, value)

            if len(self.batches[path]) < BATCH_MAX_SIZE:
                self.batches[path][row_key] = column

                # time stats
                timestamp = row_key.split('_')[1]
                print "column added to batch for %s -- %s ms" % (path, timestamp)

            elif len(self.batches[path]) == BATCH_MAX_SIZE:
                self.muse_cassandra_repo.add_batch(self.batches[path])
                self.batches[path] = {}

                # time stats
                timestamp = row_key.split('_')[1]
                print "column batch stored in cassandra for %s -- %s ms" % (path, timestamp)

    def start(self):
        self.brew.start()



if __name__ == "__main__":
    sb_client = SpacebrewClient('cloudbrain', settings.CLOUDBRAIN_ADDRESS)
    sb_client.start()
