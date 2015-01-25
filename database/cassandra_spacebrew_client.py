__author__ = 'marion'

from cassandra.cluster import Cluster

# add the shared settings file to namespace
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from settings import CLOUDBRAIN_ADDRESS
from settings import CASSANDRA_METRICS
from settings import MUSE_PORTS
from settings import CASSANDRA_SPACEBREW_NAME
from settings import CASSANDRA_IP
from spacebrew.spacebrew import SpacebrewApp
from router.spacebrew_router import SpacebrewRouter

from spacebrew_utils import calculate_spacebrew_name
import time


class CassandraSpacebrewClient(object):
    def __init__(self, name, server):

        start = time.time()

        # spacebrew router
        self.sp_router = SpacebrewRouter(server=CLOUDBRAIN_ADDRESS)

        # configure the spacebrew client
        self.brew = SpacebrewApp(name, server=server)
        for path in CASSANDRA_METRICS:
            metric_name = calculate_spacebrew_name(path)
            self.brew.add_subscriber(metric_name, "string")
            self.brew.subscribe(metric_name, self.handle_value)

            for muse_port in MUSE_PORTS:
                publisher_name = 'muse-%s' % muse_port
                self.sp_router.link(metric_name, metric_name, publisher_name, CASSANDRA_SPACEBREW_NAME,
                                    CLOUDBRAIN_ADDRESS, CASSANDRA_IP)

        # configure cassandra cluster
        self.cluster = Cluster()
        self.session = self.cluster.connect('cloudbrain')

        end = time.time()

        print 'configuration took %s s' % (end - start)

    def handle_value(self, csv_string):
        args = csv_string.split(',')

        # column family name
        osc_path = args[0]
        muse_port = args[-1]
        column_family_name = calculate_spacebrew_name(osc_path)

        # numerical values
        values = args[1:-2]
        num_arguments = len(values)
        numerical_columns = ''.join([", value_%s" % i for i in range(num_arguments)])

        # column values
        timestamp = int(time.time() * 1000)
        column_values = "'%s', '%s', %s" % (muse_port, timestamp, values[0])
        if len(values) > 1:
            for value in values[1:]:
                column_values += ", %s" % value

        insert_template = "INSERT INTO %s (muse_id, timestamp%s) VALUES (%s);"
        insert_values = insert_template % (column_family_name, numerical_columns, column_values)

        print insert_values
        self.session.execute(insert_values)

    def start(self):
        self.brew.start()


if __name__ == "__main__":
    sb_client = CassandraSpacebrewClient('cassandra', CLOUDBRAIN_ADDRESS)
    sb_client.start()
