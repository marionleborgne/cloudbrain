"""

Cient for the Muse server.

"""

import json
import socket
import time

from sandbox.muse.cassandra_repository import CassandraRepository
from cassandra_settings import KEYSPACE
from cassandra_settings import MUSE_COLUMN_FAMILY


class MuseClient(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.bind((ip, port))
        self.cassandra_repo = CassandraRepository(KEYSPACE, MUSE_COLUMN_FAMILY)

    def listen(self):
        while True:
            data, addr = self.client.recvfrom(1024)
            batch = json.loads(data)

            if batch.values()[0]['path'] == '/muse/elements/experimental/concentration':
                # todo: MuseConcentration
                pass
            elif batch.values()[0]['path'] == '/muse/elements/experimental/mellow':
                # todo: MuseMellow
                pass
            elif batch.values()[0]['path'] == '/muse/acc':
                # optional, time at which batch was received
                time_batch_received = int(time.time()*1000)
                # store batch in cassandra
                self.cassandra_repo.add_batch(batch, start_time=time_batch_received)


if __name__ == "__main__":
    obci_client = MuseClient('localhost', 5555)
    obci_client.listen()