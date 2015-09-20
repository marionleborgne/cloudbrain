"""
Cassandra Data Access Layer
"""
from cassandra.cluster import Cluster
from cloudbrain.settings import DATE_FORMAT, SENSOR_DATA_KEYSPACE
import datetime
import time
from cloudbrain.utils.metadata_info import get_num_channels



class CassandraDAO(object):
    def __init__(self):
        self.sensor_data_session = None


    def connect(self):
        """
        Connect to Cassandra cluster
        :return:
        """
        cluster = Cluster()
        self.sensor_data_session = cluster.connect(SENSOR_DATA_KEYSPACE)
        self.tags_session = cluster.connect()


    def get_data(self, device_name, device_id, metric_name, start):
        """
        Get data from Cassandra.
        :param device_name:
        :param device_id:
        :param metric_name:
        :param start:
        :return:
        """
        start_date = datetime.datetime.fromtimestamp(start).strftime(
            DATE_FORMAT)
        table_name = "%s_%s" % (device_name, metric_name)
        cql_select = ("SELECT * FROM %s WHERE device_id='%s' "
                      "AND timestamp>'%s';" % (table_name,
                                               device_id,
                                               start_date))

        rows = self.sensor_data_session.execute(cql_select)
        data = []
        for row in rows:
            device_id = row[0]
            timestamp = int(time.mktime(row[1].timetuple()) * 1000)

            record = {'device_id': device_id, 'timestamp': timestamp}

            num_channels = get_num_channels(device_name, metric_name)
            for i in xrange(num_channels):
                channel_name = "channel_%s" % i
                record[channel_name] = row[2 + i]

            data.append(record)
        return data


    def store_data(self, timestamp, device_id, device_name, metric_name,
                   channel_data):
        """
        Store data in cassandra.
        :param timestamp:
        :param device_id:
        :param device_name:
        :param metric_name:
        :param channel_data: list of channel values
        :return:
        """

        column_values = "'%s', %s" % (device_id, timestamp, )
        for channel_value in channel_data:
            column_values += ", %s" % channel_value

        num_channels = len(channel_data)
        channel_names = ["channel_%s" % i for i in xrange(num_channels)]
        column_family = "%s_%s" % (device_name, metric_name)
        columns = "device_id, timestamp, %s" % ','.join(channel_names)
        cql_insert = "INSERT INTO %s (%s) VALUES (%s);" % (column_family,
                                                           columns,
                                                           column_values)

        self.sensor_data_session.execute(cql_insert)


    def get_registered_devices(self):
        raise NotImplementedError


    def get_tag(self, tag_id):
        raise NotImplementedError


    def get_tags(self):
        raise NotImplementedError


    def create_tag(self, user_id, tag_name, metadata, start, end):
        raise NotImplemented


    def get_aggregates(self, device_id, device_type, metrics):
        raise NotImplementedError

