from consider import Consider
import time
import json
import socket


class NeuroskyServer():
  def __init__(self, sender_ip, sender_port, receiver_ip, receiver_port, user):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.sender_ip = sender_ip
    self.receiver_ip = receiver_ip
    self.receiver_port = receiver_port
    self.sender_port = sender_port
    self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.user = user

  def run(self):
    con = Consider()
    for p in con.packet_generator():
      if p.poor_signal == 0:
        timestamp = int(time.time() * 1000)
        packet = json.dumps({'meditation': p.meditation,
                             'attention': p.attention,
                             'signal_strength': p.signal,
                             'timestamp': timestamp})
        self.sock.sendto(packet, (self.receiver_ip, self.receiver_port))


if __name__ == "__main__":
  NeuroskyServer.run()