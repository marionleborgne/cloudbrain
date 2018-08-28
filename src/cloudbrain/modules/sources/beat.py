import time
import logging
import threading

from cloudbrain.modules.interface import ModuleInterface

_NANOSECONDS = 1000000
_LOGGER = logging.getLogger(__name__)

"""
Publish constant values at regular intervals on each channel.
Note that this module could be easily turned into a transformer that turns
bpm in beats by subscribing to the BPMTransformer output.
"""



def _publish(publisher, metric_name, data_to_send, bpm):
    while 1:
        publisher.publish(metric_name, data_to_send)
        beat_sleep_interval_in_s = 60.0 / bpm
        time.sleep(beat_sleep_interval_in_s)



class BeatSource(ModuleInterface):
    def __init__(self, subscribers, publishers, beat_amplitude, bpm):

        super(BeatSource, self).__init__(subscribers, publishers)
        _LOGGER.debug("Subscribers: %s" % self.subscribers)
        _LOGGER.debug("Publishers: %s" % self.publishers)
        self.beat_amplitude = beat_amplitude
        self.bpm = bpm
        self.threads = []


    def start(self):

        for publisher in self.publishers:
            for pub_metric_buffer in publisher.metric_buffers.values():
                metric_name = pub_metric_buffer.name
                num_channels = pub_metric_buffer.num_channels
                data_to_send = {'timestamp': int(time.time() * _NANOSECONDS)}
                for i in range(num_channels):
                    channel_name = 'channel_%s' % i
                    data_to_send[channel_name] = self.beat_amplitude
                t = threading.Thread(target=_publish, args=(publisher,
                                                            metric_name,
                                                            data_to_send,
                                                            self.bpm,))
                self.threads.append(t)
                t.start()


    def stop(self):
        for t in self.threads:
            t.join()
