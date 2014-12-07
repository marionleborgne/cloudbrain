DROP KEYSPACE muse;

CREATE KEYSPACE muse
WITH placement_strategy = 'SimpleStrategy'
AND strategy_options = {replication_factor : 1}
AND durable_writes = true;

USE muse;

CREATE COLUMN FAMILY acc
WITH comparator = UTF8Type
AND key_validation_class=UTF8Type
AND column_metadata = [
{column_name: path, validation_class: UTF8Type}
{column_name: acc_x, validation_class: UTF8Type}
{column_name: acc_y, validation_class: UTF8Type}
{column_name: acc_z, validation_class: UTF8Type}
{column_name: timestamp, validation_class: UTF8Type}
];



