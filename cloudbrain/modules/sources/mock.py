import logging

from cloudbrain.modules.interface import ModuleInterface
from cloudbrain.core.signal import sine_wave, signal_generator

_LOGGER = logging.getLogger(__name__)



class MockSource(ModuleInterface):
    def __init__(self, subscribers, publishers, sampling_frequency, alpha_amplitude, alpha_freq,
                 beta_amplitude, beta_freq, number_points):

        super(MockSource, self).__init__(subscribers, publishers)
        _LOGGER.debug("Subscribers: %s" % self.subscribers)
        _LOGGER.debug("Publishers: %s" % self.publishers)

        self.sampling_frequency = sampling_frequency
        self.alpha_amplitude = alpha_amplitude
        self.alpha_freq = alpha_freq
        self.beta_amplitude = beta_amplitude
        self.beta_freq = beta_freq
        self.number_points = number_points


    def start(self):

        for publisher in self.publishers:
            metrics_to_num_channels = publisher.metrics_to_num_channels()

            for (metric_name, num_channels) in metrics_to_num_channels.items():

                # Mock data for this metric
                signal = sine_wave(self.number_points,
                                   self.sampling_frequency,
                                   self.alpha_amplitude,
                                   self.alpha_freq,
                                   self.beta_amplitude,
                                   self.beta_freq)
                data = signal_generator(num_channels,
                                        self.sampling_frequency,
                                        signal)

                for datapoint in data:
                    publisher.publish(metric_name, datapoint)


    def stop(self):
        pass
