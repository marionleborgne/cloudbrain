"""

Cient for the Muse server.

"""

import json
import socket

from database.cassandra_repository import CassandraRepository
from database.cassandra_repository import convert_muse_data_to_cassandra_column
from database.cassandra_settings import KEYSPACE
from database.cassandra_settings import MUSE_COLUMN_FAMILY
from database.cassandra_settings import BATCH_MAX_SIZE


class MuseClient(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.bind((ip, port))

        # cassandra
        self.muse_cassandra_repo = CassandraRepository(KEYSPACE, MUSE_COLUMN_FAMILY)
        self.batches = {}
        self.paths = ['/muse/eeg',
                      '/muse/acc',
                      '/muse/elements/experimental/concentration',
                      '/muse/elements/experimental/mellow']
        for path in self.paths:
            self.batches[path] = {}

    def listen(self):

        while 1:
            data, addr = self.client.recvfrom(1024)
            value = json.loads(data)
            path = value[0]
            if path in self.paths:
                row_key, column = convert_muse_data_to_cassandra_column(path, value)

            if len(self.batches[path]) < BATCH_MAX_SIZE:
                self.batches[path][row_key] = column

                # time stats
                timestamp = row_key.split('_')[1]
                #print "column added to batch for %s -- %s ms" % (path, timestamp)

            elif len(self.batches[path]) == BATCH_MAX_SIZE:
                self.muse_cassandra_repo.add_batch(self.batches[path])
                self.batches[path] = {}

                # time stats
                timestamp = row_key.split('_')[1]
                print "column batch stored in cassandra for %s -- %s ms" % (path, timestamp)


if __name__ == "__main__":
    muse_client = MuseClient('localhost', 5555)
    muse_client.listen()