__author__ = 'marion'

# add the shared settings file to namespace
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from settings import DATA_VIZ_METRICS
from settings import MUSE_PORTS
from settings import SPACEBREW_DATA_VIZ_NAME
from router.spacebrew_router import SpacebrewRouter

from spacebrew_utils import calculate_spacebrew_name
import time

start = time.time()

# todo: remove these lines line
subscriber_name = SPACEBREW_DATA_VIZ_NAME
publisher_ip = '127.0.0.1'
#subscriber_ip = '50.185.173.15'
#subscriber_ip = '108.74.162.96'
subscriber_ip = '10.0.0.1'
spacebrew_server_ip = '208.66.31.59'

# spacebrew router
sp_router = SpacebrewRouter(server=spacebrew_server_ip)
for path in DATA_VIZ_METRICS:

    publisher_metric_name = calculate_spacebrew_name(path)
    for muse_port in MUSE_PORTS:

        subscriber_metric_name = '%s-%s' % (publisher_metric_name, muse_port)

        # route data FROM the muses
        publisher_name = 'muse-%s' % muse_port

        r = sp_router.link(publisher_metric_name, subscriber_metric_name, publisher_name, subscriber_name,
                            publisher_ip, subscriber_ip)
        print r

        time.sleep(0.1)

end = time.time()

print 'routing took %s s' % (end - start)


