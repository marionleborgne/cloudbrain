__author__ = 'marion'

"""
Prior to that, run:

$ ./cqlsh

DROP KEYSPACE cloudbrain;
CREATE KEYSPACE cloudbrain WITH  replication = {'class': 'SimpleStrategy', 'replication_factor': 3 };

"""


# add the shared settings file to namespace
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from cloudbrain.settings import CASSANDRA_METRICS

from cloudbrain.database.spacebrew_utils import calculate_spacebrew_name

# templates for column family creation
create_column_family_template = "CREATE TABLE %s (muse_id text, timestamp timestamp, %s PRIMARY KEY (muse_id, timestamp)); \n"
column_template = 'value_%s double, '

f = open('cassandra_schema.cql', 'w')

f.write("""DROP KEYSPACE cloudbrain;
CREATE KEYSPACE cloudbrain WITH  replication = {'class': 'SimpleStrategy', 'replication_factor': 3 };
USE cloudbrain;
""")

for path in CASSANDRA_METRICS:
    column_family_name = calculate_spacebrew_name(path)

    num_arguments = CASSANDRA_METRICS[path]
    columns = column_template % 0
    for i in range(1, num_arguments):
        columns = "%s%s" % (columns, column_template % i)
    create_column_family = create_column_family_template % (column_family_name, columns)
    f.write(create_column_family)


f.close()
