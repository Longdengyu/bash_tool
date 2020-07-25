#!/usr/bin/env python

#
# Filename: dnslog.py
# Description: dummy DNS server for outbound
# Usage: python dnslog.py
# Date Sat Jul 25 02:46:40 EDT 2020
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
    domain_splices=[]
    count_index=12
    count = int(unpack('B',req_bytes[count_index])[0])
    if count == 0:
        return None

    while count > 0:
        start = count_index + 1
        end = start + count
        count_index = end

        domain_splices.append(str(req_bytes[start:end]))

        count = int(unpack('B',req_bytes[count_index])[0])

        if count_index + count + 1 >len(req_bytes):
            return None
        elif count == 0:
            break
    return ".".join(domain_splices)

while True:
    print('\nwaiting to receive message')
    sys.stdout.flush()
    data, address = sock.recvfrom(4096)

    print('date: ' + datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    print('received %s bytes from %s' % (len(data), address))
    print("DNS request: " + parsedns(data))
    sys.stdout.flush()
