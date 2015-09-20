from cloudbrain.settings import DEVICE_METADATA


class _DeviceNameNotFound(Exception):
  pass


def map_metric_name_to_num_channels(device_name):
  """
  Map wearable metric names to the number of channels of this metric.
  :return: dict {metric_name: num_channels}
  """
  metadata = [metadata for metadata in DEVICE_METADATA if metadata['device_name'] == device_name]

  if len(metadata) > 0:
    metrics = metadata[0]['metrics']
  else:
    raise _DeviceNameNotFound("Could not find device name '%s' in metadata" % device_name)

  metric_name_to_num_channels = {}
  for metric in metrics:
    metric_name_to_num_channels[metric['metric_name']] = metric['num_channels']

  return metric_name_to_num_channels


def get_metrics_names(device_type):
  """
  Get metric names for a specific device type.
  :return: list of metric names
  """
  metadata = [metadata for metadata in DEVICE_METADATA if metadata['device_name'] == device_type]

  if len(metadata) > 0:
    metrics = metadata[0]['metrics']
  else:
    raise _DeviceNameNotFound("Could not find device name '%s' in metadata" % device_type)

  metric_names = []
  for metric in metrics:
    metric_names.append(metric['metric_name'])

  return metric_names


def get_supported_devices():
  return [device['device_name'] for device in DEVICE_METADATA]


def get_supported_metrics():
  metrics = []
  for device_name in get_supported_devices():
    metrics.extend(get_metrics_names(device_name))
  return metrics

def get_num_channels(device_name, metric):
  metric_to_channels = map_metric_name_to_num_channels(device_name)
  return metric_to_channels[metric]
