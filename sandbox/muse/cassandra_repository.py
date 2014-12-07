from sandbox.muse import cassandra_settings

__author__ = 'marion'

from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily

import logging
import time

logger = logging.getLogger()


class CassandraRepository(object):
    def __init__(self, keyspace, column_family_name):
        self.pool = ConnectionPool(keyspace,
                                   cassandra_settings.NODE_POOL)

        self.cf = ColumnFamily(self.pool, column_family_name)

        self.batch = {}

    def add_batch(self, batch, start_time=None):
        """
        :param object_list:
        """

        self.cf.batch_insert(batch)
        if start_time is not None:
            print 'time to  insert batch: %s ms' % (int(time.time() * 1000) - start_time)

        '''
        if len(self.batch) > 0 and len(self.batch) % BATCH_MAX_SIZE == 0:
            self.cf.batch_insert(self.batch)
            print 'batch inserted at %s' % int(time.time()*1000)
            self.batch = {}
        else:
            if cloudbrain_object.device == 'muse':
                row_key = str(cloudbrain_object.timestamp)
                self.batch[row_key] = cloudbrain_object.convert_for_batch()
        '''

    def get(self, timestamp):
        return self.cf.get(str(timestamp))

    def get_range(self, start, end):
        return list(self.cf.get_range(start=str(start), finish=str(end)))

    def close(self):
        self.sys.close()


if __name__ == '__main__':
    cassandra_repo = CassandraRepository(cassandra_settings.KEYSPACE, cassandra_settings.MUSE_COLUMN_FAMILY)
    batch = {}
    for i in range(100):
        batch[str(i)] = {'path': '/muse/acc',
                         'acc_x': str(i),
                         'acc_y': str(i),
                         'acc_z': str(i),
                         'timestamp': str(i)}
    cassandra_repo.add_batch(batch)
    result = cassandra_repo.get(0)
    assert result == batch[str(0)]

