DROP KEYSPACE cloudbrain;

CREATE KEYSPACE cloudbrain
WITH placement_strategy = 'SimpleStrategy'
AND strategy_options = {replication_factor : 1}
AND durable_writes = true;

USE cloudbrain;

CREATE COLUMN FAMILY muse
WITH comparator = UTF8Type
AND key_validation_class=UTF8Type
AND column_metadata = [
{column_name: path, validation_class: UTF8Type}
{column_name: values, validation_class: UTF8Type}
{column_name: timestamp, validation_class: UTF8Type}
];



