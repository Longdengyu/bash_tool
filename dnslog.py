#!/usr/bin/env python3

#
# Filename: dnslog.py
# Description: dummy DNS server for outbound
# Usage: python dnslog.py
#

import sys
import socket
from datetime import datetime as dt
from struct import unpack

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('0.0.0.0', 53)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

def parsedns(req_bytes):
    def _parsedns(req_bytes):
        count = req_bytes[0]
        if count == 0:
            return ""
        return req_bytes[1:count + 1].decode() + "." + _parsedns(req_bytes[count+1:])

    try:
        return _parsedns(req_bytes[12:])[:-1]
    except Exception as e:
        return "Error"

def dnslog_serve_forever():
    while True:
        print('\nwaiting to receive message')
        sys.stdout.flush()
        data, address = sock.recvfrom(4096)

        print('date: ' + dt.now().strftime("%Y/%m/%d %H:%M:%S"))
        print('received %s bytes from %s' % (len(data), address))
        print("DNS request: " + parsedns(data))
        sys.stdout.flush()

dnslog_serve_forever()
