import logging
import json
import sys

from cloudbrain.publishers.interface import PublisherInterface
from cloudbrain.core.model import MetricBuffer

_LOGGER = logging.getLogger(__name__)



class PipePublisher(PublisherInterface):
    """
    Publish data to named pipes. The name of the pipe is the metric routing key.
    """


    def __init__(self, base_routing_key):
        super(PipePublisher, self).__init__(base_routing_key)
        self.named_pipes = {}


    def connect(self):
        pass


    def register(self, metric_name, num_channels, buffer_size=1):
        routing_key = "%s:%s" % (self.base_routing_key, metric_name)

        # TODO: create a named pipe for each routing_key.
        # For now let's just use stdout
        self.named_pipes[routing_key] = sys.stdout

        self.metric_buffers[routing_key] = MetricBuffer(metric_name,
                                                        num_channels,
                                                        buffer_size)


    def disconnect(self):
        pass


    def publish(self, metric_name, data):
        routing_key = "%s:%s" % (self.base_routing_key, metric_name)

        # add the data to the metric buffer
        data_to_send = self.metric_buffers[routing_key].add(data)

        # publish only if you reached the max buffer size
        if data_to_send:
            message = "%s\n" % json.dumps(data_to_send)
            self.named_pipes[routing_key].write(message)
            self.named_pipes[routing_key].flush()
