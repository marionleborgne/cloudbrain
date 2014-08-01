__author__ = 'marion'

import socket


ANY = socket.gethostbyname('localhost')
self.port = 2025
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
sock.bind((ANY,self.port))
sock.setsockopt(socket.IPPROTO_IP,socket.IP_MULTICAST_TTL,255)


while 1:
    data,addr = sock.recvfrom(1024)
    print "Received message from " + str(addr) + " : " + data
    if data == "exit":
        break
sock.close()