__author__ = 'marion'

"""
Prior to that, run:

$ ./cqlsh

DROP KEYSPACE cloudbrain;
CREATE KEYSPACE cloudbrain WITH  replication = {'class': 'SimpleStrategy', 'replication_factor': 3 };

"""

from cassandra.cluster import Cluster
from cassandra import InvalidRequest

# add the shared settings file to namespace
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from settings import CASSANDRA_METRICS
from settings import CASSANDRA_IP

from spacebrew_utils import calculate_spacebrew_name


# cassandra cluster
cluster = Cluster(contact_points=[CASSANDRA_IP], port=9160)
session = cluster.connect('cloudbrain')

# templates for column family creation
create_column_family_template = "CREATE TABLE %s (muse_id text, timestamp timestamp, %s PRIMARY KEY (muse_id, timestamp));"
drop_column_family_template = "DROP TABLE %s;"
column_template = 'value_%s double, '

for path in CASSANDRA_METRICS:
    column_family_name = calculate_spacebrew_name(path)

    num_arguments = CASSANDRA_METRICS[path]
    columns = column_template % 0
    for i in range(1, num_arguments):
        columns = "%s%s" % (columns, column_template % i)
    create_column_family = create_column_family_template % (column_family_name, columns)
    drop_column_family = drop_column_family_template % column_family_name

    try:
        print drop_column_family
        session.execute(drop_column_family)
        print create_column_family
        session.execute(create_column_family)
    except InvalidRequest:
        print create_column_family
        session.execute(create_column_family)

