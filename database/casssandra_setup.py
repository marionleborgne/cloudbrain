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
import settings
from router.spacebrew_router import SpacebrewRouter

muse_osc_paths = [
            {'address': "/muse/eeg", 'arguments': 4},
            {'address': "/muse/eeg/quantization", 'arguments': 4},
            {'address': "/muse/eeg/dropped_samples", 'arguments': 1},
            {'address': "/muse/acc", 'arguments': 3},
            {'address': "/muse/acc/dropped_samples", 'arguments': 1},
            {'address': "/muse/batt", 'arguments': 4},
            {'address': "/muse/drlref", 'arguments': 2},
            {'address': "/muse/elements/low_freqs_absolute", 'arguments': 4},
            {'address': "/muse/elements/delta_absolute", 'arguments': 4},
            {'address': "/muse/elements/theta_absolute", 'arguments': 4},
            {'address': "/muse/elements/alpha_absolute", 'arguments': 4},
            {'address': "/muse/elements/beta_absolute", 'arguments': 4},
            {'address': "/muse/elements/gamma_absolute", 'arguments': 4},
            {'address': "/muse/elements/delta_relative", 'arguments': 4},
            {'address': "/muse/elements/theta_relative", 'arguments': 4},
            {'address': "/muse/elements/alpha_relative", 'arguments': 4},
            {'address': "/muse/elements/beta_relative", 'arguments': 4},
            {'address': "/muse/elements/gamma_relative", 'arguments': 4},
            {'address': "/muse/elements/delta_session_score", 'arguments': 4},
            {'address': "/muse/elements/theta_session_score", 'arguments': 4},
            {'address': "/muse/elements/alpha_session_score", 'arguments': 4},
            {'address': "/muse/elements/beta_session_score", 'arguments': 4},
            {'address': "/muse/elements/gamma_session_score", 'arguments': 4},
            {'address': "/muse/elements/touching_forehead", 'arguments': 1},
            {'address': "/muse/elements/horseshoe", 'arguments': 4},
            {'address': "/muse/elements/is_good", 'arguments': 4},
            {'address': "/muse/elements/blink", 'arguments': 1},
            {'address': "/muse/elements/jaw_clench", 'arguments': 1},
            {'address': "/muse/elements/experimental/concentration", 'arguments': 1},
            {'address': "/muse/elements/experimental/mellow", 'arguments': 1}
        ]

def calculate_spacebrew_name(osc_path):
        spacebrew_name = osc_path.split('/')[-1]
        return disambiguate_name_collisions(spacebrew_name, osc_path)


def disambiguate_name_collisions(spacebrew_name, osc_path):
    if spacebrew_name == 'dropped_samples':
        return osc_path.split('/')[-2] + '_' + osc_path.split('/')[-1]
    else:
        return spacebrew_name


# spacebrew router
sp_router = SpacebrewRouter(server=settings.CLOUDBRAIN_ADDRESS)

# cassandra cluster
cluster = Cluster()
session = cluster.connect('cloudbrain')

# templates for column family creation
create_column_family_template = "CREATE TABLE %s (muse_id text, timestamp timestamp, %s PRIMARY KEY (muse_id, timestamp));"
drop_column_family_template = "DROP TABLE %s;"
column_template = 'value_%s double, '

for path in muse_osc_paths:
    column_family_name = calculate_spacebrew_name(path['address'])

    num_arguments = path['arguments']
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

    for muse_id in settings.MUSE_IPS:
        sp_router.link(column_family_name, column_family_name, 'muse-%s' % muse_id, 'cassandra', settings.MUSE_IPS[muse_id], settings.CASSANDRA_IP)
