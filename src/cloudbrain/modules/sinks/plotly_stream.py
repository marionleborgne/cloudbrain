import json
import logging
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls

from cloudbrain.modules.interface import ModuleInterface

_LOGGER = logging.getLogger(__name__)


class PlotlyStreamSink(ModuleInterface):
    def __init__(self, subscribers, publishers, max_points=100,
                 ignore_time=False):

        super(PlotlyStreamSink, self).__init__(subscribers, publishers)
        _LOGGER.debug("Subscribers: %s" % self.subscribers)
        _LOGGER.debug("Publishers: %s" % self.publishers)

        self.max_points = max_points
        self.ignore_time = ignore_time
        self.stream_ids = []
        self.py_streams = []
        self.go_streams = []
        self.points_streamed = 0

    def start(self):
        for subscriber in self.subscribers:
            for metric_buffer in subscriber.metric_buffers.values():
                _LOGGER.info('Subscribing to %s' % metric_buffer.name)

                local_stream_ids = tls.get_credentials_file()['stream_ids']
                if len(local_stream_ids) < metric_buffer.num_channels:
                    raise ValueError(
                        "Not enough stream tokens. Required: %s. Actual: %s. "
                        "Add a stream token to 'stream_ids' in your "
                        "~/.plotly/.credentials file. More details "
                        "at https://plot.ly/python/getting-started/"
                        % (metric_buffer.num_channels, len(local_stream_ids)))
                self.setup_metric_streams(local_stream_ids, metric_buffer.name,
                                          metric_buffer.num_channels)

                callback = self._callback_factory(metric_buffer.num_channels)
                subscriber.subscribe(metric_buffer.name, callback)

    def _callback_factory(self, num_channels):

        def callback(unused_ch, unused_method, unused_properties, body):

            for data in json.loads(body):
                x = data['timestamp']
                for channel_idx in range(num_channels):
                    channel_name = 'channel_%s' % channel_idx
                    y = data[channel_name]
                    self.write_to_stream(channel_idx, x, y)

        return callback

    def setup_metric_streams(self, local_stream_ids, metric_name, num_channels):

        for i in range(num_channels):
            stream_id = local_stream_ids[i]
            self.stream_ids.append(stream_id)
            py_stream = py.Stream(stream_id)
            py_stream.open()
            self.py_streams.append(py_stream)

            go_stream = go.Stream(token=stream_id, maxpoints=self.max_points)
            self.go_streams.append(go_stream)

        traces = []
        for i in range(num_channels):
            channel_name = "channel_%s" % i
            go_stream = self.go_streams[i]

            trace = go.Scatter(
                x=[],
                y=[],
                mode='splines',
                stream=go_stream,
                name=channel_name
            )
            traces.append(trace)

        data = go.Data(traces)
        layout = go.Layout(title=metric_name)
        fig = go.Figure(data=data, layout=layout)
        py.iplot(fig, filename=metric_name)

    def write_to_stream(self, channel_idx, x, y):

        s = self.py_streams[channel_idx]
        # Write numbers to stream to append current data on plot,
        # write lists to overwrite existing data on plot
        if self.ignore_time:
            s.write(dict(x=self.points_streamed, y=y))
        else:
            s.write(dict(x=x, y=y))

        self.points_streamed += 1

    def stop(self):
        # Close the streams when done plotting
        for s in self.py_streams:
            s.close()
