import json
import logging
from liblo import ServerThread, make_method

from cloudbrain.connectors.museio import _start_muse_io

_LOGGER = logging.getLogger(__name__)
_LOGGER.level = logging.DEBUG
_LOGGER.addHandler(logging.StreamHandler())



class MuseConnector(ServerThread):
    """
    Get OSC messages from the Muse
    """


    def __init__(self, ip, port, start_muse_io, callback_functions):
        ServerThread.__init__(self, port)
        self.callback_functions = callback_functions
        if start_muse_io:
            _start_muse_io(port)


    # receive EEG data
    @make_method('/muse/eeg', 'f' * 8)
    def eeg_callback(self, path, args):
        self.callback_functions['eeg'](json.dumps([path, args]))


    # receive horseshoe data
    @make_method("/muse/elements/horseshoe", 'f' * 8)
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
