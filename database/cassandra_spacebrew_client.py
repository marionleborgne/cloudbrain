__author__ = 'marion'

from cassandra.cluster import Cluster

# add the shared settings file to namespace
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from settings import EXPLO_BRAINSERVER_IP
from settings import CASSANDRA_METRICS
from settings import MUSE_PORTS
from settings import SPACEBREW_CASSANDRA_NAME
from spacebrew.spacebrew import SpacebrewApp

from spacebrew_utils import calculate_spacebrew_name
import time


class CassandraSpacebrewClient(object):
    def __init__(self, name, server):

        start = time.time()

        # configure cassandra cluster
        self.cluster = Cluster()
        self.session = self.cluster.connect('cloudbrain')


        # configure the spacebrew client
        self.brew = SpacebrewApp(name, server=server)
        for path in CASSANDRA_METRICS:
            publisher_metric_name = calculate_spacebrew_name(path)
            for muse_port in MUSE_PORTS:

                # add subscriber
                subscriber_metric_name = '%s-muse-%s' % (publisher_metric_name, muse_port)
                self.brew.add_subscriber(subscriber_metric_name, "string")

                # handle value
                handle_value = self.handle_value_factory(publisher_metric_name, muse_port)
                self.brew.subscribe(subscriber_metric_name, handle_value)


        end = time.time()

        print 'configuration took %s s' % (end - start)

    def handle_value_factory(self, metric, muse_port):

        def handle_value(csv_string):

            values = csv_string.split(',')

            # numerical values
            num_arguments = len(values)
            numerical_columns = ''.join([", value_%s" % i for i in range(num_arguments)])

            # column values
            timestamp = int(time.time() * 1000)
            column_values = "'%s', '%s', %s" % (muse_port, timestamp, values[0])
            if len(values) > 1:
                for value in values[1:]:
                    column_values += ", %s" % value

            insert_template = "INSERT INTO %s (muse_id, timestamp%s) VALUES (%s);"
            insert_values = insert_template % (metric, numerical_columns, column_values)

            print insert_values
            self.session.execute(insert_values)

        return handle_value

    def start(self):
        self.brew.start()


if __name__ == "__main__":
    sb_client = CassandraSpacebrewClient(SPACEBREW_CASSANDRA_NAME, EXPLO_BRAINSERVER_IP)
    sb_client.start()
