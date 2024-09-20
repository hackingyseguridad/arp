#!/bin/bash
# Cambio de MAC Address en periferico de red
# ifconfig eth0 hw ether 00:e0:4c:53:44:58
# Otra opcion es con macchanger
# apt-get install macchanger
# macchanger -m 00:e0:4c:53:44:58 eth0
# Otra Opcion es con IP
# sudo ip link set eth0 down
# ip link set eth0 address 00:e0:4c:53:44:58
# sudo ip link set eth0 up
#
# hackingyseguridad.com ( 2024 )
#

sudo ifconfig eth0 down
sudo ifconfig eth0 hw ether 00:e0:4c:53:44:58
sudo ifconfig eth0 down

# Actualizar IP con HDCP para la nueva MAC 
# dhclient eth0

ip link show eth0 | grep ether | awk '{print $2}'




