"""
Cassandra Data Access Layer
"""

import uuid
import datetime
import time

from cassandra.cluster import Cluster
from cloudbrain.settings import (DATE_FORMAT,
                                 ANALYTICS_KEYSPACE,
                                 SENSOR_DATA_KEYSPACE,
                                 TAGS_TABLE_NAME,
                                 AGGREGATES_TABLE_NAME)
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
        self.analytics_session = cluster.connect(ANALYTICS_KEYSPACE)


    def get_data(self, device_name, device_id, metric_name, start):
        """
        Get data from Cassandra.
        :param device_name:
        :param device_id:
        :param metric_name:
        :param start:
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


    def store_data(self, timestamp, device_id, device_name, metric_name, channel_data):
        """
        Store data in cassandra.
        :param timestamp:
        :param device_id:
        :param device_name:
        :param metric_name:
        :param channel_data: list of channel values
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


    def get_registered_devices(self, user_id):
        raise NotImplementedError


    def get_tag(self, user_id, tag_id):
        """ Get the registered devices IDs for a user """
        raise NotImplementedError


    def get_tags(self, user_id, tag_name):
        if tag_name is not None:
            cql_select = ("SELECT * FROM %s WHERE user_id='%s' AND tag_name='%s' ALLOW FILTERING;"
                          % (TAGS_TABLE_NAME, user_id, tag_name))
        else:
            cql_select = ("SELECT * FROM %s WHERE user_id='%s' ALLOW FILTERING;"
                          % (TAGS_TABLE_NAME, user_id))

        rows = self.analytics_session.execute(cql_select)

        data = []
        for row in rows:
            tag_id = row[0]
            user_id = row[1]
            tag_name = row[2]
            metadata = row[4]
            if row[3] is not None:
                end = int(time.mktime(row[3].timetuple()) * 1000)
            else:
                end = None
            if row[5] is not None:
                start = int(time.mktime(row[5].timetuple()) * 1000)
            else:
                start = None

            record = {"tag_id": tag_id,
                      "user_id": user_id,
                      "tag_name": tag_name,
                      "metadata": metadata,
                      "end": end,
                      "start": start
            }

            data.append(record)
        return data


    def create_tag(self, user_id, tag_name, metadata, start, end):
        tag_id = str(uuid.uuid4())
        columns = "tag_id, user_id, tag_name, start"
        values = "'%s', '%s', '%s', '%s'" % (tag_id, user_id, tag_name, start)
        if end is not None:
            columns += ", end"
            values += ", %s" % end
        if metadata is not None:
            columns += ", metadata"
            values += ", '%s'" % metadata

        cql_insert = "INSERT INTO %s (%s) VALUES (%s);" % (TAGS_TABLE_NAME,
                                                           columns,
                                                           values)

        self.analytics_session.execute(cql_insert)
        return tag_id


    def get_aggregates(self, user_id, tag_id, device_type, metrics):
        raise NotImplementedError

