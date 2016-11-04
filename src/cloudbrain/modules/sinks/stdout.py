import json
import logging

from cloudbrain.modules.interface import ModuleInterface

_LOGGER = logging.getLogger(__name__)



def _print_callback(unsed_ch, unsed_method, unsed_properties, body):
    print("==> %s\n" % body)



class StdoutSink(ModuleInterface):
    def __init__(self, subscribers, publishers):

        super(StdoutSink, self).__init__(subscribers, publishers)
        _LOGGER.debug("Subscribers: %s" % self.subscribers)
        _LOGGER.debug("Publishers: %s" % self.publishers)


    def start(self):
        for subscriber in self.subscribers:
            for metric_buffer in subscriber.metric_buffers.values():
                _LOGGER.info('Subscribing to %s' % metric_buffer.name)
                subscriber.subscribe(metric_buffer.name, _print_callback)
