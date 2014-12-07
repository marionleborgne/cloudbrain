create keyspace cloudbrain
  with placement_strategy = 'NetworkTopologyStrategy'
  and strategy_options = {datacenter1 : 1}
  and durable_writes = true;

use cloudbrain;

create column family muse
  with column_type = 'Standard'
  and comparator = 'BytesType'
  and default_validation_class = 'BytesType'
  and key_validation_class = 'BytesType'
  and read_repair_chance = 0.0
  and dclocal_read_repair_chance = 0.1
  and populate_io_cache_on_flush = false
  and gc_grace = 864000
  and min_compaction_threshold = 4
  and max_compaction_threshold = 32
  and replicate_on_write = true
  and compaction_strategy = 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy'
  and caching = 'KEYS_ONLY'
  and default_time_to_live = 0
  and speculative_retry = 'NONE'
  and compression_options = {'sstable_compression' : 'org.apache.cassandra.io.compress.LZ4Compressor'}
  and index_interval = 128;

assume muse keys as ascii;
assume muse comparator as ascii;
assume muse validator as ascii;
assume muse sub_comparator as ascii;