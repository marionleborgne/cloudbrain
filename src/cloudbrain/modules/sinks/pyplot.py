import json
import logging

import matplotlib.pyplot as plt
import numpy as np

from cloudbrain.modules.interface import ModuleInterface

_LOGGER = logging.getLogger(__name__)



class PyPlotSink(ModuleInterface):
    def __init__(self,
                 subscribers,
                 publishers,
                 channels_to_plot,
                 autoscale=True,
                 y_min=-15,
                 y_max=15):

        super(PyPlotSink, self).__init__(subscribers, publishers)
        _LOGGER.debug("Subscribers: %s" % self.subscribers)
        _LOGGER.debug("Publishers: %s" % self.publishers)

        self.channels_to_plot = channels_to_plot
        self.autoscale = autoscale
        self.y_min = y_min,
        self.y_max = y_max
        self.extra = 0
        self.count = 0
        self.N_points = 200
        self.data = [0 for i in range(self.N_points)]

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

        # Init X and Y data
        self.x = np.arange(self.N_points)
        self.y = self.data
        self.li, = self.ax.plot(self.x, self.data)

        # draw and show it
        self.fig.canvas.draw()
        plt.show(block=False)

        if len(self.channels_to_plot) > 1:
            raise ValueError("At the moment the PyPlotSink module does not "
                             "support plotting multiple channels.\n"
                             "The number of channels is %s.\n"
                             "Please check the JSON config file to make sure "
                             "there's only one." % len(self.channels_to_plot))

        if len(self.subscribers) > 1:
            raise ValueError("At the moment the PyPlotSink module does not s"
                             "upport plotting from multiple subscribers.\n"
                             "The number of subscribers is %s.\n"
                             "Please check the JSON config file to make sure "
                             "there's only one." % len(self.subscribers))

        for subscriber in subscribers:
            num_metrics = len(subscriber.metric_buffers)
            if num_metrics > 1:
                raise ValueError(
                    "At the moment the PyPlotSink module does not support "
                    "plotting multiple metrics.\n"
                    "The number of metrics of a subscriber is %s.\n"
                    "Please check the JSON config file to make sure there's "
                    "only one." % num_metrics)


    def start(self):

        for i in range(len(self.subscribers)):
            for subscriber in self.subscribers:
                for metric_buffer in subscriber.metric_buffers.values():
                    metric_name = metric_buffer.name
                    # TODO: needs to be changed. Right now this is only good
                    # for 1 metric + channel
                    subscriber.subscribe(metric_name, self._consume_metric)


    def _update_plot(self):

        self.li.set_ydata(self.data)

        self.ax.relim()
        if self.autoscale:
            self.ax.autoscale_view(True, True, True)
        else:
            self.ax.set_ylim([self.y_min, self.y_max])

        self.fig.canvas.draw()
        plt.draw()
        plt.pause(0.0001)  # Don't render too fast


    def _consume_metric(self, connection, deliver, properties, msg_s):

        msg = json.loads(msg_s)
        d = []
        for row in msg:
            d.append(float(row['channel_0']))
        self.data.extend(d)

        self.data = self.data[- self.N_points - self.extra:]
        self._update_plot()
