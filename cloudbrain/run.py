import argparse
import subprocess
import sys

from cloudbrain.publishers.sensor_publisher import get_args_parser, run


def publish(args):
  parser = get_args_parser()

  opts = parser.parse_args(args)

  mock_data_enabled = opts.mock
  device_name = opts.device_name
  device_id = opts.device_id
  cloudbrain_address = opts.cloudbrain
  buffer_size = opts.buffer_size
  device_port = opts.device_port
  pipe_name = opts.output
  publisher = opts.publisher

  run(device_name,
   mock_data_enabled,
   device_id,
   cloudbrain_address,
   buffer_size,
   device_port,
   pipe_name,
   publisher)

def subscribe():
  raise NotImplemented("Subscribe is not implemented")

def parse_args():
  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers()

  publish_parser = subparsers.add_parser('publish',
                      help="Publish data stream - For example: cloudbrain publish --mock -n muse -i octopicorn")
  publish_parser.set_defaults(func=publish)

  subscribe_parser = subparsers.add_parser('subscribe',
                      help="Subscribe to data stream - For example: cloudbrain subscribe -n muse -i octopicorn")
  subscribe_parser.set_defaults(func=subscribe)

  args, remaining_args = parser.parse_known_args()
  args.func(remaining_args)

def main():
  parse_args()

if __name__ == "__main__":
  main()
