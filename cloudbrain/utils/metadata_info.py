from cloudbrain.settings import DEVICE_METADATA

def map_metric_to_num_channels(device_name):
  """
  Map wearable metric names to the number of channels of this metric.
  :return: dict {metric_name: num_channels}
  """
  metadata = [metadata for metadata in DEVICE_METADATA if metadata['device_name'] == device_name][0]

  metric_name_to_num_channels = {}
  for metric in metadata['metrics']:
    metric_name_to_num_channels[metric['metric_name']] = metric['num_channels']

  return metric_name_to_num_channels

def get_metrics_names(device_name):
  """
  Get metric names for a specific device name.
  :return: list of metric names
  """
  metadata = [metadata for metadata in DEVICE_METADATA if metadata['device_name'] == device_name][0]

  metric_names = []
  for metric in metadata['metrics']:
    metric_names.append(metric['metric_name'])

  return metric_names
