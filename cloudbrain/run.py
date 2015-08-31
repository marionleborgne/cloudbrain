import argparse
import subprocess
import sys

import cloudbrain.publishers.sensor_publisher

def publish(args):
    sys.argv = args or ['-h']
    cloudbrain.publishers.sensor_publisher.main()

def subscribe(args):
    return NotImplemented

def parse_args():
  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers()

  publish_parser = subparsers.add_parser('publish',
                      help="Publish data stream - For example: cloudbrain publish --mock -n muse -i octopicorn")
  publish_parser.set_defaults(func=publish)

  subscribe_parser = subparsers.add_parser('subscribe',
                      help="Subscribe to data stream - For example: cloudbrain subscribe -n muse -i octopicorn")
  subscribe_parser.set_defaults(func=subscribe)

  args, unknown = parser.parse_known_args()
  args.func(unknown)

def main():
    parse_args()

if __name__ == "__main__":
  main()
