__author__ = 'marion'

# add the shared settings file to namespace
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from settings import EXPLO_BRAINSERVER_IP
from settings import CASSANDRA_METRICS
from settings import MUSE_PORTS
from settings import SPACEBREW_CASSANDRA_NAME
from settings import SPACEBREW_CASSANDRA_IP
from settings import SPACEBREW_BRAINSERVER_IP
from router.spacebrew_router import SpacebrewRouter

from spacebrew_utils import calculate_spacebrew_name
import time


start = time.time()

# spacebrew router
sp_router = SpacebrewRouter(server=EXPLO_BRAINSERVER_IP)
for path in CASSANDRA_METRICS:

    publisher_metric_name = calculate_spacebrew_name(path)
    for muse_port in MUSE_PORTS:

        subscriber_metric_name = '%s-muse-%s' % (publisher_metric_name, muse_port)

        # route data
        publisher_name = 'muse-%s' % muse_port
        subscriber_name = SPACEBREW_CASSANDRA_NAME

        r = sp_router.link(publisher_metric_name, subscriber_metric_name, publisher_name, subscriber_name,
                            SPACEBREW_BRAINSERVER_IP, SPACEBREW_CASSANDRA_IP)
        print r

        time.sleep(0.1)

end = time.time()

print 'routing took %s s' % (end - start)


