__author__ = 'marion'

# add the shared settings file to namespace
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
from cloudbrain.settings import DATA_VIZ_METRICS
from cloudbrain.settings import MUSE_PORTS
from cloudbrain.settings import SPACEBREW_DATA_VIZ_NAME
from cloudbrain.router.spacebrew_router import SpacebrewRouter

from cloudbrain.spacebrew.spacebrew_utils import calculate_spacebrew_name
import time

start = time.time()

# todo: remove these lines line
subscriber_name = SPACEBREW_DATA_VIZ_NAME
publisher_ip = '107.170.205.177'
subscriber_ip = '10.0.0.245'
spacebrew_server_ip = '107.170.205.177'

# spacebrew router
sp_router = SpacebrewRouter(server=spacebrew_server_ip)
for path in DATA_VIZ_METRICS:

    publisher_metric_name = calculate_spacebrew_name(path)
    for muse_port in MUSE_PORTS:

        subscriber_metric_name = '%s-muse-%s' % (publisher_metric_name, muse_port)

        # route data FROM the muses
        publisher_name = 'muse-%s' % muse_port

        r = sp_router.link(publisher_metric_name, subscriber_metric_name, publisher_name, subscriber_name,
                            publisher_ip, subscriber_ip)
        print r

        time.sleep(0.1)

end = time.time()

print 'routing took %s s' % (end - start)


