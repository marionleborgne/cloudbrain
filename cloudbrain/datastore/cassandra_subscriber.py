import json
import argparse
import threading

from cloudbrain.subscribers.PikaSubscriber import PikaSubscriber
from cloudbrain.datastore.CassandraDAO import CassandraDAO
from cloudbrain.settings import MOCK_DEVICE_ID, RABBITMQ_ADDRESS
from cloudbrain.utils.metadata_info import (get_supported_metrics,
                                            get_supported_devices,
                                            get_num_channels,
                                            get_metrics_names)

_SUPPORTED_DEVICES = get_supported_devices()
_SUPPORTED_METRICS = get_supported_metrics()



class CassandraSubscriber(object):
    """
    Subscribes and writes data to a file
    """


    def __init__(self, device_type, device_id, rabbitmq_address):
        self.subscribers = {}
        self.rabbitmq_address = rabbitmq_address
        self.device_type = device_type
        self.device_id = device_id
        self.cassandra_dao = CassandraDAO()
        self.threads = []


    def start(self):
        self.cassandra_dao.connect()
        metrics = get_metrics_names(self.device_type)
        for metric in metrics:
            self.subscribers[metric] = PikaSubscriber(
                device_name=self.device_type,
                device_id=self.device_id,
                rabbitmq_address=self.rabbitmq_address,
                metric_name=metric)
            self.subscribers[metric].connect()

            t = threading.Thread(target=self.subscribers[metric].consume_messages,
                                 args=(self.write_to_cassandra_factory(metric),))
            self.threads.append(t)
            t.start()


    def stop(self):
        for subscriber in self.subscribers:
            subscriber.disconnect()


    def write_to_cassandra_factory(self, metric):

        num_channels = get_num_channels(self.device_type, metric)


        def write_to_cassandra(ch, method, properties, body):
            buffer_content = json.loads(body)
            for record in buffer_content:
                timestamp = record["timestamp"]
                channel_data = [record["channel_%s" % i] for i in
                                xrange(num_channels)]

                self.cassandra_dao.store_data(timestamp,
                                              self.device_id,
                                              self.device_type,
                                              metric,
                                              channel_data)


        return write_to_cassandra



def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--device_id', required=True,
                        help="A unique ID to identify the device you are sending data from. "
                             "For example a MAC address")
    parser.add_argument('-n', '--device_name', required=True,
                        help="The name of the device your are sending data from. "
                             "Supported devices are: %s" % _SUPPORTED_DEVICES)
    parser.add_argument('-c', '--cloudbrain', default=RABBITMQ_ADDRESS,
                        help="The address of the CloudBrain instance you are sending data to.\n "
                             "Use %s to send data to our hosted service. \n Otherwise use "
                             "'localhost' if running CloudBrain locally" % RABBITMQ_ADDRESS)

    opts = parser.parse_args()
    return opts



def main():
    opts = parse_args()

    device_name = opts.device_name
    device_id = opts.device_id
    cloudbrain_address = opts.cloudbrain

    run(device_name,
        device_id,
        cloudbrain_address)



def run(device_name='muse',
        device_id=MOCK_DEVICE_ID,
        cloudbrain_address=RABBITMQ_ADDRESS):
    print "Storing data to Cassandra ... Ctl-C to stop."

    # TODO: need to differentiate between cassandra address and rabbitMQ address.
    cassandra_subscriber = CassandraSubscriber(device_type=device_name,
                                               device_id=device_id,
                                               rabbitmq_address=cloudbrain_address)
    cassandra_subscriber.start()



if __name__ == "__main__":
    #main()
    run()
