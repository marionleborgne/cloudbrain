__author__ = 'marion'

# log file
LOG_FILE = "cassandra_repository.log"

# cassandra config
PORT = 9160
NODE_IP = '127.0.0.1'
NODE_POOL = ['%s:%s' % (NODE_IP, PORT)]
BATCH_MAX_SIZE = 10

### muse ###

# keyspace
KEYSPACE = 'cloudbrain'

# column families
MUSE_COLUMN_FAMILY = 'muse'
# example:
# row_key = timestamp
# row = {'acc_x' = <double>, 'acc_x' = <double>, 'acc_x' = <double>}

MUSE_EEG = 'eeg'
# example:
# row_key = timestamp
# row = {...}

MUSE_CONCENTRATION = 'concentration'
# example:
# row_key = timestamp
# row = {'concentration' = <double>}

MUSE_MELLOW = 'mellow'
# example:
# row_key = timestamp
# row = {'mellow'}

### OpenBCI ###

# keyspace
OPENBCI_KEYSPACE = 'openbci'

# column families
OPENBCI_RAW = 'raw_data'  # raw channel data
# example:
# row_key = timestamp
# row = {channel_1: <double>, ..., channel_7: <double>, timestamp: <long>}

### Neurosky ###

# keyspace
NEUROSKY_KEYSPACE = 'neurosky'

# column families
NEUROSKY_CONSIDER = 'consider'  # data from the Consider protocol (by ThinkGear)
# example:
# row_key = timestamp
# row = {meditation: <double>, attention: <double>, signal: <double>}


