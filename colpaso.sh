#!/bin/bash
while
  set $(dd if=/dev/urandom bs=4 count=1 2>/dev/null | od -An -tu1)
  [ $1 -lt 224 ] &&
  [ $1 -ne 10 ] &&
  { [ $1 -ne 192 ] || [ $2 -ne 168 ]; } &&
  { [ $1 -ne 172 ] || [ $2 -lt 16 ] || [ $2 -gt 31 ]; }
arp -i eth0 -s $ip_address 00:11:22:BB:CC:EE
do :; done
ip_address=$1.$2.$3.$4
echo $ip_address
