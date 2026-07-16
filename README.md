# ARP — Herramientas de ARP Spoofing y Análisis de Red

![Shell](https://img.shields.io/badge/Shell-37.1%25-89e051)
![Python](https://img.shields.io/badge/Python-62.9%25-3572A5)
![Licencia](https://img.shields.io/badge/uso-educativo-orange)

Colección de scripts en **Bash** y **Python** para practicar y entender técnicas de **ARP Spoofing (envenenamiento ARP)**, cambio de dirección MAC, escaneo de red y ataques de tipo Man-in-the-Middle (MITM) a nivel de capa de enlace. Pensado como material didáctico para pruebas en **entornos de laboratorio controlados**.

> 🌐 Más recursos en [hackingyseguridad.com](http://www.hackingyseguridad.com/)

---

## 📑 Índice

1. [Aviso legal y ético](#-aviso-legal-y-ético)
2. [Fundamentos: ¿qué es ARP Spoofing?](#-fundamentos-qué-es-arp-spoofing)
3. [Estructura del repositorio](#-estructura-del-repositorio)
4. [Requisitos previos](#-requisitos-previos)
5. [Instalación](#-instalación)
6. [Guía de uso por script](#-guía-de-uso-por-script)
7. [Tabla comparativa de scripts](#-tabla-comparativa-de-scripts)
8. [Detección y contramedidas](#-detección-y-contramedidas)
9. [Limitaciones conocidas](#-limitaciones-conocidas)
10. [Buenas prácticas de laboratorio](#-buenas-prácticas-de-laboratorio)
11. [Contribuciones](#-contribuciones)
12. [Autor y créditos](#-autor-y-créditos)

---

## ⚠️ Aviso legal y ético

Estas herramientas manipulan el protocolo ARP para interceptar o redirigir tráfico de red. Utilizarlas contra redes, dispositivos o personas **sin autorización explícita** puede constituir un delito (en España, entre otros, bajo los artículos del Código Penal relativos a delitos informáticos y de interceptación de comunicaciones).

| Uso permitido | Uso prohibido |
|---|---|
| Laboratorios propios o máquinas virtuales aisladas | Redes de terceros sin permiso |
| Auditorías de seguridad con contrato/autorización por escrito | Redes públicas, universitarias o corporativas ajenas |
| Formación y CTF (Capture The Flag) | Interceptar comunicaciones de otras personas sin consentimiento |
| Entornos de pruebas de laboratorio (GNS3, VirtualBox, VMware) | Cualquier entorno de producción sin autorización |

El autor del repositorio y esta documentación **no se hacen responsables del mal uso** de estas herramientas.

---

## 📘 Fundamentos: ¿qué es ARP Spoofing?

El protocolo **ARP (Address Resolution Protocol)** traduce direcciones IP a direcciones MAC dentro de una red local. No incluye ningún mecanismo de autenticación, por lo que un atacante puede enviar respuestas ARP falsas (*ARP spoofing* o *ARP poisoning*) para que otros equipos actualicen su tabla ARP con una MAC incorrecta.

| Concepto | Descripción |
|---|---|
| **ARP Request/Reply** | Mensajes que asocian una IP a una MAC en la LAN |
| **ARP Spoofing** | Envío de respuestas ARP falsificadas para suplantar una IP |
| **Gratuitous ARP** | Anuncio ARP no solicitado, útil para forzar la actualización de tablas ARP de toda la red |
| **MITM (Man-in-the-Middle)** | Situar el equipo atacante entre víctima y puerta de enlace para interceptar tráfico |
| **IP Forwarding** | Necesario para que la víctima no pierda conectividad mientras el atacante reenvía el tráfico |

---

## 🗂 Estructura del repositorio

| Archivo | Lenguaje | Tipo de técnica | Descripción breve |
|---|---|---|---|
| `arpspoof.sh` | Bash | ARP Spoofing bidireccional | Envenena la tabla ARP de dos hosts entre sí usando la herramienta `arpspoof` (dsniff) |
| `mitm.py` | Python (Scapy) | MITM manual | Construye y envía paquetes ARP falsificados a víctima y gateway para interceptar tráfico |
| `gratuitousarp.py` | Python (Scapy) | Gratuitous ARP | Envía anuncios ARP gratuitos en bucle usando Scapy |
| `flood.py` | Python (Scapy) | ARP Flood | Genera un envío continuo de paquetes ARP hacia un objetivo |
| `colpasoarp.sh` | Bash | Manipulación de tabla ARP | Genera una IP aleatoria válida y la añade a la tabla ARP local con una MAC fija |
| `cambiarmac.sh` | Bash | Cambio de MAC | Modifica la dirección MAC de una interfaz de red |
| `scanmac.sh` | Bash | Reconocimiento | Escanea un rango de IPs y lista las direcciones MAC asociadas mediante `nmap` |

---

## 🧰 Requisitos previos

| Herramienta | Instalación (Debian/Ubuntu/Kali) | Usada por |
|---|---|---|
| `dsniff` (arpspoof) | `sudo apt-get install dsniff` | `arpspoof.sh` |
| `nmap` | `sudo apt-get install nmap` | `scanmac.sh` |
| `python2` + `scapy` | `sudo apt-get install python2 python2-pip && pip2 install scapy` | `mitm.py`, `gratuitousarp.py`, `flood.py` |
| `net-tools` (ifconfig) | `sudo apt-get install net-tools` | `cambiarmac.sh` |
| `iproute2` (ip) | Incluido por defecto en la mayoría de distros | `colpasoarp.sh`, `cambiarmac.sh` |
| `macchanger` (opcional) | `sudo apt-get install macchanger` | Alternativa mencionada en `cambiarmac.sh` |

> 🔑 Casi todos los scripts requieren **privilegios de root**, ya que manipulan interfaces de red, tablas ARP y el reenvío de paquetes IP (`ip_forward`).

---

## ⚙️ Instalación

```bash
git clone https://github.com/hackingyseguridad/arp.git
cd arp
chmod +x *.sh
```

Para los scripts en Python (compatibles con **Python 2**, ver [Limitaciones conocidas](#-limitaciones-conocidas)):

```bash
sudo pip2 install scapy
```

---

## 📖 Guía de uso por script

### 🔹 `arpspoof.sh` — Spoofing ARP bidireccional

Activa el reenvío de IP y lanza dos procesos `arpspoof` en paralelo para envenenar simultáneamente a la víctima y a la puerta de enlace, colocando el equipo atacante en medio del tráfico.

```bash
sudo ./arpspoof.sh <interfaz> <IP_víctima> <IP_gateway>
# Ejemplo:
sudo ./arpspoof.sh eth0 192.168.1.252 192.168.1.250
```

Pulsa cualquier tecla para detener el ataque; el script mata los procesos y restaura `ip_forward` a `0`.

### 🔹 `mitm.py` — MITM manual con Scapy

Descubre la MAC de la víctima y de la puerta de enlace (resolviendo la IP pública de `www.google.com` vía ICMP), y después envía paquetes ARP falsificados a ambas partes en bucle, activando `ip_forward` para mantener la conectividad.

```bash
sudo python2 mitm.py
# Solicitará interactivamente la IP objetivo
```

> Requiere editar manualmente `my_ip` y `my_mac` en el script para adaptarlos a tu interfaz.

### 🔹 `gratuitousarp.py` — Gratuitous ARP en bucle

Envía de forma continua paquetes ARP "gratuitous" (no solicitados) usando Scapy. Útil para forzar la actualización de tablas ARP en la red o para pruebas de detección de IDS/ARPwatch.

```bash
sudo python2 gratuitousarp.py
```

### 🔹 `flood.py` — Inundación ARP dirigida

Solicita interactivamente la interfaz de red y la IP objetivo, detecta automáticamente la puerta de enlace y la MAC local, y envía paquetes ARP cada 0.5 segundos de forma indefinida.

```bash
sudo python2 flood.py
# Input egress interface: eth0
# Input target IP: 192.168.1.50
```

### 🔹 `colpasoarp.sh` — Entrada ARP con IP aleatoria

Genera una dirección IP aleatoria válida (excluyendo multicast, redes privadas típicas y direcciones reservadas) y añade una entrada estática a la tabla ARP local (`ip neigh`) asociándola a una MAC ficticia.

```bash
sudo ./colpasoarp.sh
```

### 🔹 `cambiarmac.sh` — Cambio de dirección MAC

Desactiva la interfaz `eth0`, le asigna una nueva MAC y la muestra por pantalla. El propio script documenta como comentario dos métodos alternativos: `macchanger` y `ip link set`.

```bash
sudo ./cambiarmac.sh
```

> ✏️ Edita la variable de MAC (`00:e0:4c:53:44:58`) y el nombre de interfaz dentro del script antes de ejecutarlo.

### 🔹 `scanmac.sh` — Escaneo de IP/MAC en la red

Ejecuta un `nmap -sn` (ping scan) sobre un rango de IPs y muestra en formato `IP => MAC` todos los hosts detectados, ordenados alfabéticamente.

```bash
sudo ./scanmac.sh 192.168.1.0/24
```

---

## 📊 Tabla comparativa de scripts

| Script | Requiere root | Interactivo | Modifica `ip_forward` | Riesgo de interrupción de red |
|---|:---:|:---:|:---:|:---:|
| `arpspoof.sh` | ✅ | No | ✅ | Medio |
| `mitm.py` | ✅ | ✅ | ✅ | Medio-Alto |
| `gratuitousarp.py` | ✅ | No | ❌ | Alto |
| `flood.py` | ✅ | ✅ | ❌ | Alto |
| `colpasoarp.sh` | ✅ | No | ❌ | Bajo |
| `cambiarmac.sh` | ✅ | No | ❌ | Bajo |
| `scanmac.sh` | ✅ | No | ❌ | Ninguno |

---

## 🛡 Detección y contramedidas

| Técnica de detección | Descripción |
|---|---|
| **IDS de red** | Un sistema de detección de intrusiones bien configurado puede alertar ante picos anómalos de tráfico ARP |
| **Sniffers (Wireshark)** | Permiten inspeccionar en tiempo real respuestas ARP duplicadas o inconsistentes |
| **ARPwatch** | Monitoriza cambios en la tabla ARP y avisa ante asociaciones IP-MAC inesperadas |
| **DHCP Snooping / Dynamic ARP Inspection** | Funciones de switches gestionables que validan las respuestas ARP contra una tabla de confianza |
| **Entradas ARP estáticas** | En hosts críticos, fijar manualmente la entrada ARP del gateway evita el envenenamiento |
| **Segmentación de red (VLANs)** | Reduce el alcance de un ataque de ARP Spoofing al limitar el dominio de difusión |

Señales típicas de un ataque en curso: pérdida intermitente de conectividad, lentitud repentina, o duplicidad de direcciones MAC reportada por el sistema operativo.

---

## 🧩 Limitaciones conocidas

- **Python 2 obsoleto:** `mitm.py` y `flood.py` usan `raw_input()` y el módulo `commands` (eliminado en Python 3). Requieren Python 2, que ya no recibe soporte oficial; se recomienda migrarlos a Python 3 con `input()` y `subprocess`.
- **IPs/MACs codificadas:** `mitm.py` contiene valores de ejemplo (`my_ip`, `my_mac`) que deben editarse manualmente para cada entorno.
- **Interfaz fija:** `cambiarmac.sh` asume `eth0`; en sistemas con nombres de interfaz predecibles (`enp0s3`, `wlan0`, etc.) hay que adaptarlo.
- **Sin gestión de errores robusta:** la mayoría de los scripts no valida argumentos ni maneja excepciones más allá de un `try/except` básico.
- **Sin limpieza automática en algunos casos:** `gratuitousarp.py` y `flood.py` no restauran el estado de red al finalizar (a diferencia de `arpspoof.sh`).

---

## ✅ Buenas prácticas de laboratorio

1. Usa siempre una **red virtual aislada** (VirtualBox/VMware en modo "solo anfitrión" o una VLAN de pruebas dedicada).
2. Documenta la MAC/IP originales antes de modificarlas para poder revertir los cambios.
3. Restaura `ip_forward` a `0` y elimina entradas ARP manuales al terminar las pruebas.
4. No ejecutes estos scripts en redes compartidas (Wi-Fi de coworking, universidad, empresa) sin autorización expresa.

---

## 🤝 Contribuciones

Las *pull requests* son bienvenidas, especialmente para:
- Migrar los scripts Python 2 a Python 3.
- Añadir manejo de errores y validación de argumentos.
- Incorporar detección automática de interfaz/gateway.

---

## 👤 Autor y créditos

- Repositorio mantenido por [hackingyseguridad](https://github.com/hackingyseguridad) — [hackingyseguridad.com](http://www.hackingyseguridad.com/)
- `colpasoarp.sh` incluye crédito original a *Antonio Taboada (2018)*.
