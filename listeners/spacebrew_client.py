__author__ = 'marion'

# add the shared settings file to namespace
import sys
from os.path import dirname, abspath

sys.path.insert(0, dirname(dirname(abspath(__file__))))
import settings

from spacebrew.spacebrew import SpacebrewApp
from database.cassandra_repository import CassandraRepository
from database.cassandra_repository import convert_muse_data_to_cassandra_column
from database.cassandra_settings import KEYSPACE
from database.cassandra_settings import MUSE_COLUMN_FAMILY
from database.cassandra_settings import BATCH_MAX_SIZE

import json


class SpacebrewClient(object):
    def __init__(self, name, server, store_in_cassandra=False):
        # configure the spacebrew client
        self.brew = SpacebrewApp(name, server=server)

        # cassandra
        if store_in_cassandra:
            self.muse_cassandra_repo = CassandraRepository(KEYSPACE, MUSE_COLUMN_FAMILY)
            self.batches = {}
        self.paths = ['/muse/eeg',
                      '/muse/acc',
                      '/muse/elements/experimental/concentration',
                      '/muse/elements/experimental/mellow']

        for path in self.paths:
            spacebrew_name = path.split('/')[-1]
            self.brew.add_subscriber(spacebrew_name, "string")
            if store_in_cassandra:
                self.batches[path] = {}
                self.brew.subscribe(spacebrew_name, self.handle_value_cassandra)
            else:
                self.brew.subscribe(spacebrew_name, self.handle_value)


    def handle_value(self, string_value):
        value = json.loads(string_value)
        print value

    def handle_value_cassandra(self, string_value):
        value = json.loads(string_value)
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
    sb_client = SpacebrewClient('cloudbrain', settings.CLOUDBRAIN_ADDRESS, store_in_cassandra=False)
    sb_client.start()
