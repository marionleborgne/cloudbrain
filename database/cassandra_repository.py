__author__ = 'marion'
import cassandra_settings
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily

import logging
import time

logger = logging.getLogger()


def convert_muse_data_to_cassandra_column(osc_path, data):
    timestamp = int(time.time() * 1000)
    row_key = '%s_%s' % (osc_path, timestamp)
    column = {'path': osc_path,
              'values': str(data[1:]),
              'timestamp': str(timestamp)}

    return row_key, column


class CassandraRepository(object):
    def __init__(self, keyspace, column_family_name):
        self.pool = ConnectionPool(keyspace,
                                   cassandra_settings.NODE_POOL)

        self.cf = ColumnFamily(self.pool, column_family_name)

        self.batch = {}

    def add_batch(self, batch, start_time=None):
        """
        :param batch:
        """

        self.cf.batch_insert(batch)
        if start_time is not None:
            print 'time to  insert batch: %s ms' % (int(time.time() * 1000) - start_time)


    def get(self, timestamp):
        return self.cf.get(str(timestamp))

    def get_range(self, start, end):
        return list(self.cf.get_range(start=str(start), finish=str(end)))

    def close(self):
        self.sys.close()


if __name__ == '__main__':
    muse_cassandra_repo = CassandraRepository(cassandra_settings.KEYSPACE, cassandra_settings.MUSE_COLUMN_FAMILY)
    batch = {}
    for i in range(100):
        batch[str(i)] = {'path': '/muse/acc',
                         'values': str([i, i, i]),
                         'timestamp': str(i)}
    muse_cassandra_repo.add_batch(batch)
    result = muse_cassandra_repo.get(0)
    assert result == batch[str(0)]

