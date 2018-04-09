#!/bin/bash
echo "Escanea y lista las IP = MAC Address"
echo "Uso.: #sh scanmac.sh rango_IP"
sudo nmap -sn $1 | awk '/Nmap scan report for/{printf $5;}/MAC Address:/{print " => "$3;}' | sort
