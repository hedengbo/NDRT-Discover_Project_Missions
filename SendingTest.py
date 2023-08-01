# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 23:13:03 2017

@author: heden
"""

import socket
from struct import pack

while 1:
    UDP_IP = "192.168.14.2"
    UDP_PORT = 1228
    MESSAGE = 1234556
    buff = pack('<i', MESSAGE)
       
    print "UDP target IP:", UDP_IP
    print "UDP target port:", UDP_PORT
    print "message:", MESSAGE
       
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.sendto(buff, (UDP_IP, UDP_PORT))