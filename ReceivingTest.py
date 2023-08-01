# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 11:03:04 2017

@author: heden
"""
import socket
from struct import unpack

UDP_IP = "90.0.0.50"
UDP_PORT = 1228
 
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
 
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    show = unpack('<i', data)
    print "received message:", show