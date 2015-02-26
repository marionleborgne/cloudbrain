"""
Muse Server for Recording to Disk.

Note that MuseIO SDK is required

To start MuseIO, open a terminal or command prompt and type:

muse-io --osc osc.udp://localhost:9090

"""

__author__ = 'cyb3rnetic'

from liblo import ServerThread, ServerError, make_method
import json
import sys
import time


# add the shared settings file to namespace
import sys
from os.path import dirname, abspath

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))


class DiskOutServer(ServerThread):
    def __init__(self, muse_port, began_at):
        # Configuring the Muse OSC client
        ServerThread.__init__(self, muse_port)

        self.began_at = began_at

        self.osc_paths = [
            {'address': "/muse/eeg", 'arguments': 4},
            {'address': "/muse/eeg/quantization", 'arguments': 4},
            {'address': "/muse/eeg/dropped_samples", 'arguments': 1},
            {'address': "/muse/acc", 'arguments': 3},
            {'address': "/muse/acc/dropped_samples", 'arguments': 1},
            {'address': "/muse/batt", 'arguments': 4},
            {'address': "/muse/drlref", 'arguments': 2},
            {'address': "/muse/elements/low_freqs_absolute", 'arguments': 4},
            {'address': "/muse/elements/delta_absolute", 'arguments': 4},
            {'address': "/muse/elements/theta_absolute", 'arguments': 4},
            {'address': "/muse/elements/alpha_absolute", 'arguments': 4},
            {'address': "/muse/elements/beta_absolute", 'arguments': 4},
            {'address': "/muse/elements/gamma_absolute", 'arguments': 4},
            {'address': "/muse/elements/delta_relative", 'arguments': 4},
            {'address': "/muse/elements/theta_relative", 'arguments': 4},
            {'address': "/muse/elements/alpha_relative", 'arguments': 4},
            {'address': "/muse/elements/beta_relative", 'arguments': 4},
            {'address': "/muse/elements/gamma_relative", 'arguments': 4},
            {'address': "/muse/elements/delta_session_score", 'arguments': 4},
            {'address': "/muse/elements/theta_session_score", 'arguments': 4},
            {'address': "/muse/elements/alpha_session_score", 'arguments': 4},
            {'address': "/muse/elements/beta_session_score", 'arguments': 4},
            {'address': "/muse/elements/gamma_session_score", 'arguments': 4},
            {'address': "/muse/elements/touching_forehead", 'arguments': 1},
            {'address': "/muse/elements/horseshoe", 'arguments': 4},
            {'address': "/muse/elements/is_good", 'arguments': 4},
            {'address': "/muse/elements/blink", 'arguments': 1},
            {'address': "/muse/elements/jaw_clench", 'arguments': 1},
            {'address': "/muse/elements/experimental/concentration", 'arguments': 1},
            {'address': "/muse/elements/experimental/mellow", 'arguments': 1}
        ]

        self.paths = [path['address'] for path in self.osc_paths]


    def close(self):
        self.stop()


    # handle all messages if the OSC path is in self.paths
    @make_method(None, None)
    def fallback(self, path, args, types, src):

        if path in self.paths:
            spacebrew_name = path.split('/')[-1]
            elapsed = time.time() - self.began_at

            data = {
                'time': elapsed - 90,
                'name': spacebrew_name,
                'data': ",".join([str(i) for i in args])
            }

            if elapsed > 90 and elapsed < 100:
                print json.dumps(data), ","
            elif elapsed > 100:
                print "]"
                server.stop()
                sys.exit()

if __name__ == "__main__":
    try:
        print "["
        server = DiskOutServer(9090, time.time())
    except ServerError, err:
        print str(err)
        sys.exit()

    try:
        server.start()
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        print "]"
        sys.exit()


