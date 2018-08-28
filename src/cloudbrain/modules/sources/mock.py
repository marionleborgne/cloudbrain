import logging
import threading

from cloudbrain.modules.interface import ModuleInterface
from cloudbrain.core.signal import sine_wave, signal_generator

_LOGGER = logging.getLogger(__name__)



def _publish_data(publisher, metric_name, datapoints):
    for datapoint in datapoints:
        publisher.publish(metric_name, datapoint)




class MockSource(ModuleInterface):
    def __init__(self,
                 subscribers,
                 publishers,
                 sampling_frequency,
                 alpha_amplitude,
                 alpha_freq,
                 beta_amplitude,
                 beta_freq,
                 notch_amplitude,
                 notch_freq,
                 noise_amplitude,
                 number_points):

        super(MockSource, self).__init__(subscribers, publishers)
        _LOGGER.debug("Subscribers: %s" % self.subscribers)
        _LOGGER.debug("Publishers: %s" % self.publishers)

        self.sampling_frequency = sampling_frequency
        self.alpha_amplitude = alpha_amplitude
        self.alpha_freq = alpha_freq
        self.beta_amplitude = beta_amplitude
        self.beta_freq = beta_freq
        self.notch_amplitude = notch_amplitude
        self.notch_freq = notch_freq
        self.noise_amplitude = noise_amplitude
        self.number_points = number_points

        self.threads = []


    def start(self):

        # Mock data for this metric
        signal = sine_wave(self.number_points,
                           self.sampling_frequency,
                           self.alpha_amplitude,
                           self.alpha_freq,
                           self.beta_amplitude,
                           self.beta_freq,
                           self.notch_amplitude,
                           self.notch_freq)

        for publisher in self.publishers:
            metrics_to_num_channels = publisher.metrics_to_num_channels()

            # start a thread per metric to not block the main thread
            for (metric_name, num_channels) in metrics_to_num_channels.items():
                data = signal_generator(num_channels,
                                        self.sampling_frequency,
                                        signal, self.noise_amplitude)

                t = threading.Thread(target=_publish_data,
                                     args=(publisher, metric_name, data))
                t.daemon = True
                self.threads.append(t)
                t.start()


    def stop(self):
        for t in self.threads:
            t.join(0)
