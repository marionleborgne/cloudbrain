from liblo import ServerThread, ServerError, make_method
import sys
import time
import json


class MuseOSC(ServerThread):
  """
  Getting OSC messages from the Muse
  """

  def __init__(self, muse_port, callback_functions):
    ServerThread.__init__(self, muse_port)
    self.callback_functions = callback_functions

  # receive EEG data
  @make_method('/muse/eeg', 'ffff')
  def eeg_callback(self, path, args):
    self.callback_functions['eeg'](json.dumps([path, args]))

  # receive horseshoe data
  @make_method("/muse/elements/horseshoe", 'ffff')
  def horseshoe_callback(self, path, args):
    self.callback_functions['horseshoe'](json.dumps([path, args]))

  # receive concentration data
  @make_method('/muse/elements/experimental/concentration', 'f')
  def concentration_callback(self, path, args):
    self.callback_functions['concentration'](json.dumps([path, args]))

  # receive meditation data
  @make_method('/muse/elements/experimental/mellow', 'f')
  def mellow_callback(self, path, args):
    self.callback_functions['mellow'](json.dumps([path, args]))

  # handle unexpected messages
  @make_method(None, None)
  def fallback(self, path, args, types, src):
    pass  # do nothing for now


def _print_callback(sample):
  """
  Callback function handling Muse samples
  :return:
  """

  print sample


if __name__ == "__main__":

  callbacks = {'eeg': _print_callback,
               'concentration': _print_callback,
               'mellow': _print_callback,
               'horseshoe': _print_callback}

  print ("[INFO] To start MuseIO, open a terminal or command prompt and run:\n"
         "muse-io --osc osc.udp://localhost:9090")

  try:
    server = MuseOSC(9090, callbacks)
  except ServerError, err:
    print str(err)
    sys.exit()

  try:
    server.start()
    while 1:
      time.sleep(1)
  except KeyboardInterrupt:
    sys.exit()
