#!/bin/bash

#
#  Description: socks5 local server by ssh
# 
#  Note: for the safety you can use public key authentication by adding your 
#   rsa pub key to .ssh/authorized_keys, then adding directives to the pub key 
#   like this 'restrict,port-forwarding,command="/bin/false" ssh-rsa AAAAB3NzaC1...'
#


REMOTE_USER=<user>
REMOTE_HOST=<host>
REMOTE_PORT=<port>

trap exit SIGINT 
trap exit SIGTERM

while true
do 
    echo running netcat guard
    echo this is netcat guard | nc -lvp 1080

    echo running ssh socks5
    ssh -D 0.0.0.0:1080  -C -q -N $REMOTE_USER@$REMOTE_HOST -p $REMOTE_PORT
    echo
done

