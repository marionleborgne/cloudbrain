"""
Muse Server.

Note that both Spacebrew and the MuseIO SDK are required

Spacebrew installation:
* git clone https://github.com/Spacebrew/spacebrew
* follow the readme instructions to install and start spacebrew

To start MuseIO, open a terminal or command prompt and type:

muse-io --osc osc.udp://localhost:9090

"""

__author__ = 'marion'

from liblo import ServerThread, make_method
import json

# add the shared settings file to namespace
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))
import settings

from spacebrew.spacebrew import SpacebrewApp


class SpacebrewServer(ServerThread):

    def __init__(self, muse_port, muse_id, server):
        # Configuring the Muse OSC client
        ServerThread.__init__(self, muse_port)

        # configure the Spacebrew client
        self.brew = SpacebrewApp(muse_id, server=server)

        self.paths = ['/muse/eeg',
                      '/muse/acc',
                      '/muse/elements/experimental/concentration',
                      '/muse/elements/experimental/mellow']

        for path in self.paths:
            spacebrew_name = path.split('/')[-1]
            self.brew.add_publisher(spacebrew_name, "string")

        # connect to spacebrew
        self.brew.start()


    def close(self):
        self.brew.stop()
        self.stop()

    # receive accelerometer data
    @make_method('/muse/acc', 'fff')
    def acc_callback(self, path, args):
        data = [path] + args

        sb_name = path.split('/')[-1]
        self.brew.publish(sb_name, json.dumps(data))


    # receive EEG data
    @make_method('/muse/eeg', 'ffff')
    def eeg_callback(self, path, args):
        data = [path] + args

        sb_name = path.split('/')[-1]
        self.brew.publish(sb_name, json.dumps(data))

    # receive concentration data
    @make_method('/muse/elements/experimental/concentration', 'f')
    def concentration_callback(self, path, args):
        data = [path] + args
        sb_name = path.split('/')[-1]
        self.brew.publish(sb_name, json.dumps(data))

    # receive meditation data
    @make_method('/muse/elements/experimental/mellow', 'f')
    def mellow_callback(self, path, args):
        data = [path] + args

        sb_name = path.split('/')[-1]
        self.brew.publish(sb_name, json.dumps(data))


    # handle unexpected messages
    @make_method(None, None)
    def fallback(self, path, args, types, src):
        # do nothing for now ...
        pass


if __name__ == "__main__":
    server = SpacebrewServer(9090, 'muse-example', settings.CLOUDBRAIN_ADDRESS)
    server.start()

