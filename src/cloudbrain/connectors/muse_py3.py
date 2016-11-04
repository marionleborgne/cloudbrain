import logging
from pythonosc import osc_server, dispatcher

from cloudbrain.connectors.museio import _start_muse_io

_LOGGER = logging.getLogger(__name__)
_LOGGER.level = logging.DEBUG
_LOGGER.addHandler(logging.StreamHandler())



class MuseConnector(object):
    """
    Get OSC messages from the Muse
    """


    def __init__(self, ip, port, start_muse_io, callback_functions):
        self.port = port
        self.ip = ip
        self.callback_functions = callback_functions
        if start_muse_io:
            _start_muse_io(port)


    def start(self):
        muse_dispatcher = dispatcher.Dispatcher()
        for metric_name in self.callback_functions:
            callback = self.callback_functions[metric_name]
            _LOGGER.info('Mapping %s' % metric_name)
            muse_dispatcher.map("/muse/%s" % metric_name, callback,
                                metric_name)

        _LOGGER.debug('Dispatcher: %s' % muse_dispatcher)
        server = osc_server.ThreadingOSCUDPServer(
            (self.ip, self.port), muse_dispatcher)
        print("Serving on {}".format(server.server_address))
        server.serve_forever()
