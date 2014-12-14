__author__ = 'marion'

from spacebrew.spacebrew import SpacebrewApp
import json


class SpacebrewClient(object):

    def __init__(self, name, server):

        # configure the spacebrew client
        self.brew = SpacebrewApp(name, server=server)
        self.paths = ['/muse/eeg',
                      '/muse/acc',
                      '/muse/elements/experimental/concentration',
                      '/muse/elements/experimental/mellow']

        for path in self.paths:
            spacebrew_name = path.split('/')[-1]
            self.brew.add_subscriber(spacebrew_name, "string")
            self.brew.subscribe(spacebrew_name, self.handle_value)

    def handle_value(self, string_value):
        value = json.loads(string_value)
        print value

    def start(self):
        self.brew.start()


if __name__ == "__main__":
    sb_client = SpacebrewClient('cloudbrain', '127.0.0.1')
    sb_client.start()
