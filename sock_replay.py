#!/usr/bin/env python

#
# filename: sock_replay.py
#
# description: generate accepted socket replay python script from strace log
#
# date: 2020/12/14
#
# usage:  sock_replay.py <stracelog>
#
# example:
#
# 1. do strace as this: 
#	strace -f -y -s 10000 -o strace.log -xx
# 2. sock_replay.py strace.log 
#

import sys



def usage():
	help = """
filename: sock_replay.py

description: generate accepted socket replay python script from strace log

date: 2020/12/14

usage:  sock_replay.py <stracelog>

example:

1. do strace as this: 
      strace -f -y -s 10000 -o strace.log -xx
2. sock_replay.py strace.log 

"""
	sys.stderr.write(help)

if len(sys.argv) != 2:
	usage()
	sys.exit(0)
strace_log = sys.argv[1]

def handle_write(line):
	count = line.strip().split(" ")[-1]
	payload = line.split(", ")[1]
	print("conn.{0}({1})".format("write", payload))

def handle_sendto(line):
	count = line.strip().split(" ")[-1]
	payload = line.split(", ")[1]
	print("conn.{0}({1})".format("sendto", payload))

def handle_read(line):
	count = line.strip().split(" ")[-1]
	print("conn.{0}({1})".format("read", count))

def handle_recvfrom(line):
	count = line.strip().split(" ")[-1]
	print("conn.{0}({1})".format("recvfrom", count))

handler_map = {
	"read": handle_read,
	"recvfrom": handle_recvfrom,
	"write": handle_write,
	"sendto": handle_sendto
}

sock_string = None
with open(strace_log, "r") as f:
	for line in f:
		if "accept" in line:
			sock_string = line.strip().split("= ")[1].split("<")[1].split(">")[0]
			break
if not sock_string:
	sys.exit(-1)

with open(strace_log, "r") as f:
	for line in f:
		if not sock_string in line:
			continue
		line = line.strip()
		syscall_name = line.split('<')[0].split(" ")[2].split("(")[0]
		if syscall_name in handler_map:
			handler_map[syscall_name](line)
