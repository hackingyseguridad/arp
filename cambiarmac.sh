# Cambio de MAC Address en periferico de red
# ifconfig eth0 hw ether 00:e0:4c:53:44:58
# Otra opcion es con macchanger
# apt-get install macchanger
# macchanger -m 00:e0:4c:53:44:58 eth0
#
# hackingyseguridad.com ( 2024 )
#

sudo ifconfig eth0 down
sudo ifconfig eth0 hw ether 00:e0:4c:53:44:58
sudo ifconfig eth0 down

# Actualizar IP con HDCP para la nueva MAC 
# dhclient eth0
