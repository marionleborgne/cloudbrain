_DEVICE_ID = "my_device"
_DEVICE_NAME = "muse"
_HOST = "localhost"
_BUFFER_SIZE = 100





if __name__ == "__main__":
  subscriber = PikaSubscriber(_DEVICE_NAME, _DEVICE_ID, _HOST)
  subscriber.connect()
  subscriber.consume_messages(_print_message)
