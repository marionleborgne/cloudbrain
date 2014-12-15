"""

Client for the OpenBCI server.

"""

import json
import socket


class OpenBCIClient(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.bind((ip, port))

    def listen(self):
        while True:
            data, addr = self.client.recvfrom(1024)
            sample = json.loads(data)
            print sample
            # todo: store in DB

if __name__ == "__main__":
    obci_client = OpenBCIClient('localhost', 5555)
    obci_client.listen()