from os.path import realpath
from cloudbrain.settings import (DEVICE_METADATA,
                                 USERS_KEYSPACE,
                                 USERS_CONSENT_TABLE,
                                 SENSOR_DATA_KEYSPACE,
                                 ANALYTICS_KEYSPACE,
                                 TAGS_TABLE_NAME,
                                 AGGREGATES_TABLE_NAME)

# template for keyspace creation
_CREATE_KEYSPACE = ("DROP KEYSPACE %s;\n"
                    "CREATE KEYSPACE %s WITH replication = "
                    "{'class': 'SimpleStrategy', 'replication_factor': 3 };\n"
                    "USE %s;")



def _create_users_keyspace_and_table(outFile):
    """
    Create users keyspace and tables
    @param outFile: file to write CQL statements to
    """
    create_keyspace = _CREATE_KEYSPACE % (USERS_KEYSPACE,
                                          USERS_KEYSPACE,
                                          USERS_KEYSPACE)
    create_table = ("CREATE TABLE %s (user_id text, timestamp timestamp, "
                    "consent text, age double, gender text, "
                    "PRIMARY KEY (user_id));\n") % USERS_CONSENT_TABLE

    outFile.write(create_keyspace)
    outFile.write("\n")
    outFile.write(create_table)
    outFile.write("\n")



def _create_device_metadata_table(outFile, device_name):
    """
    Create device metadata tables
    @param outFile: file to write CQL statements to
    @param device_name: name of the device
    """
    metadata_table_name = "%s_metadata" % device_name
    create_table = ("CREATE TABLE %s "
                    "(device_id text, user_id text, timestamp timestamp, "
                    "sampling_rate float, electrode_placement text, "
                    "PRIMARY KEY (device_id));\n") % metadata_table_name

    outFile.write(create_table)



def _create_tags_table(outFile):
    """
    Create tag table
    @param outFile: file to write CQL statements to
    """
    create_table = ("CREATE TABLE %s "
                    "(device_id text, user_id text, timestamp timestamp, "
                    "sampling_rate float, electrode_placement text, "
                    "PRIMARY KEY (device_id));\n") % TAGS_TABLE_NAME

    outFile.write(create_table)



def _create_sensor_data_keyspace_and_table(outFile):
    """
    Create sensor data keyspace and tables
    @param outFile: file to write CQL statements to
    """
    # templates for column family creation
    create_column_family_template = ("CREATE TABLE %s "
                                     "(device_id text, timestamp timestamp, %s "
                                     "PRIMARY KEY (device_id, timestamp)); \n")
    column_template = 'channel_%s double, '

    create_keyspace = _CREATE_KEYSPACE % (SENSOR_DATA_KEYSPACE,
                                          SENSOR_DATA_KEYSPACE,
                                          SENSOR_DATA_KEYSPACE)
    outFile.write(create_keyspace)
    outFile.write("\n")

    for device in DEVICE_METADATA:

        device_name = device['device_name']

        metrics = device['metrics']
        for metric in metrics:
            metric_name = metric['metric_name']
            num_arguments = metric['num_channels']

            columns = column_template % 0
            for i in range(1, num_arguments):
                columns = "%s%s" % (columns, column_template % i)

            # The column family name is a compound of the device name
            # and metric name
            column_family_name = "%s_%s" % (device_name, metric_name)
            create_column_family = create_column_family_template % (
                column_family_name, columns)
            outFile.write(create_column_family)

        _create_device_metadata_table(outFile, device_name)

        outFile.write("\n")



def _create_analytics_keyspace_and_table(outFile):
    """
    Create analytics keyspace and tables
    @param outFile: file to write CQL statements to
    """
    create_keyspace = _CREATE_KEYSPACE % (ANALYTICS_KEYSPACE,
                                          ANALYTICS_KEYSPACE,
                                          ANALYTICS_KEYSPACE)

    create_tags_table = ("CREATE TABLE %s (tag_id text, tag_name text, user_id text, "
                         "start timestamp, end timestamp, metadata text, "
                         "PRIMARY KEY (tag_id, user_id, tag_name));\n") % TAGS_TABLE_NAME

    create_aggregates_table = ("CREATE TABLE %s (aggregate_id text, user_id text, "
                               "tag_id text, device_type text, aggregate_type text, "
                               "aggregate_value float, metric text, start timestamp, end timestamp, "
                               "PRIMARY KEY (user_id));\n") % AGGREGATES_TABLE_NAME

    outFile.write(create_keyspace)
    outFile.write("\n")
    outFile.write(create_tags_table)
    outFile.write(create_aggregates_table)
    outFile.write("\n")



def main():
    """
    Generate cassandra schema
    """
    with open('cassandra_schema.cql', 'w') as f:
        _create_sensor_data_keyspace_and_table(f)
        _create_users_keyspace_and_table(f)
        _create_analytics_keyspace_and_table(f)

        schema_path = realpath('cassandra_schema.cql')
        print "\nSUCCESS: Schema generated. Now run: cqlsh -f %s" % schema_path



if __name__ == "__main__":
    main()


