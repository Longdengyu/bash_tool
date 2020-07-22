#!/usr/bin/env python

import socket

HOST = 'localhost'
PORT = 6379
socket.setdefaulttimeout(0.5)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))
while True:
    cmd = raw_input("redis> ").strip()
    if cmd == "readline":
        try:
            print(s.makefile().readline())
        except Exception:
            pass
    else:
        s.send(cmd+"\r\n")
        print(s.makefile().readline())
