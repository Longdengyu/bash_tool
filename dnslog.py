#!/usr/bin/env python

#
# Filename: dnslog.py
# Description: dummy DNS server for outbound
# Usage: python dnslog.py
# Date: Mon Jul 27 02:48:02 EDT 2020
#

import sys
import socket
from datetime import datetime
from struct import unpack

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('0.0.0.0', 53)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

def parsedns(req_bytes):
    if len(req_bytes) < 1:
        return "";
    count = int(unpack('B',req_bytes[0])[0])
    if count == 0:
        return ""
    if count > len(req_bytes) -1:
        return ""
    return req_bytes[1:count + 1] + "." + parsedns(req_bytes[count+1:])

while True:
    print('\nwaiting to receive message')
    sys.stdout.flush()
    data, address = sock.recvfrom(4096)
    if len(data) < 13:
        continue

    print('date: ' + datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    print('received %s bytes from %s' % (len(data), address))
    print("DNS request: " + parsedns(data[12:]))
    sys.stdout.flush()
