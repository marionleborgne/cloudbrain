__author__ = 'marion'


"""
To create the schema, run: ./cqlsh -f <path_to_file>/cassandra_schema.cql
"""


# add the shared settings file to namespace
import sys
from os.path import dirname, abspath, realpath
sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
from cloudbrain.settings import DEVICE_METADATA


# template for keyspace creation  
create_keyspace_template = """DROP KEYSPACE %s;
CREATE KEYSPACE %s WITH  replication = {'class': 'SimpleStrategy', 'replication_factor': 3 };
USE %s;
"""

# templates for column family creation
create_column_family_template = "CREATE TABLE %s (user_id text, timestamp timestamp, %s PRIMARY KEY (user_id, timestamp)); \n"
column_template = 'value_%s double, '


# generate cassandra schema
f = open('cassandra_schema.cql', 'w')
for device in DEVICE_METADATA:
  
  device_name = device['device_name']
  # The keyspace name is the name of the device
  create_keyspace = create_keyspace_template % (device_name, device_name, device_name)
  f.write(create_keyspace)
  
  
  metrics = device['metrics']
  for metric in metrics:
    metric_name = metric['metric_name']
    num_arguments = metric['num_channels']

    columns = column_template % 0
    for i in range(1, num_arguments):
        columns = "%s%s" % (columns, column_template % i)
    
    # The column family name is the metric name
    create_column_family = create_column_family_template % (metric_name, columns)
    f.write(create_column_family)
    
  f.write("\n")


f.write("""
DROP KEYSPACE users;
CREATE KEYSPACE users WITH  replication = {'class': 'SimpleStrategy', 'replication_factor': 3 };
USE users;
CREATE TABLE consent (user_id text, timestamp timestamp, consent text, age double, gender text,  PRIMARY KEY (user_id, timestamp));
""")

schema_path = realpath('cassandra_schema.cql')
print "Schema generated. Run: ./cqlsh -f %s" % schema_path

f.close()


