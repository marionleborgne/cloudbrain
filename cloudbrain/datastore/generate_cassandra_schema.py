from os.path import realpath
from cloudbrain.settings import DEVICE_METADATA, SENSOR_DATA_KEYSPACE, REGISTERED_DEVICES_TABLE_NAME

# template for keyspace creation
create_keyspace_template = ("DROP KEYSPACE %s;\n"
                            "CREATE KEYSPACE %s WITH replication = "
                            "{'class': 'SimpleStrategy', 'replication_factor': 3 };\n"
                            "USE %s;")


# templates for column family creation
create_column_family_template = ("CREATE TABLE %s (device_id text, "
                                 "timestamp timestamp, %s PRIMARY KEY (device_id, timestamp)); \n")
column_template = 'channel_%s double, '

# generate cassandra schema
with open('cassandra_schema.cql', 'w') as f:
  create_keyspace = create_keyspace_template % (SENSOR_DATA_KEYSPACE,
                                                SENSOR_DATA_KEYSPACE,
                                                SENSOR_DATA_KEYSPACE)
  f.write(create_keyspace)

  for device in DEVICE_METADATA:

    device_name = device['device_name']

    metrics = device['metrics']
    for metric in metrics:
      metric_name = metric['metric_name']
      num_arguments = metric['num_channels']

      columns = column_template % 0
      for i in range(1, num_arguments):
        columns = "%s%s" % (columns, column_template % i)

      # The column family name is a compound of the device name and metric name
      column_family_name = "%s_%s" % (device_name, metric_name)
      create_column_family = create_column_family_template % (column_family_name, columns)
      f.write(create_column_family)

    f.write("\n")

    registered_devices = ("CREATE TABLE %s (device_id text, "
                          "device_name text, timestamp timestamp, "
                          "PRIMARY KEY (device_id, timestamp));") % REGISTERED_DEVICES_TABLE_NAME

  f.write("CREATE TABLE % (user_id text, timestamp timestamp, consent text, age double, gender text,  "
          "PRIMARY KEY (user_id));\n"
          "DROP KEYSPACE users;\n"
          "CREATE KEYSPACE users WITH  replication = {'class': 'SimpleStrategy',"
          " 'replication_factor': 3 };\n"
          "USE users;\n"
          "CREATE TABLE consent "
          "(user_id text, timestamp timestamp, consent text, age double, gender text,  "
          "PRIMARY KEY (user_id, timestamp));\n")

  schema_path = realpath('cassandra_schema.cql')
  print "\nSUCCESS: Schema generated. Now run: cqlsh -f %s" % schema_path




