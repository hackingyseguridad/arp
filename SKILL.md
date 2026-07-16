---
name: arp-lab-toolkit
description: Ayuda a preparar, ejecutar y documentar prácticas de ARP Spoofing, cambio de MAC, escaneo de red y ataques MITM a nivel ARP usando los scripts del repositorio hackingyseguridad/arp, exclusivamente en laboratorios propios o entornos con autorización explícita para pruebas de seguridad. Úsalo cuando el usuario mencione "ARP spoofing", "envenenamiento ARP", "arpspoof.sh", "cambiar MAC", "escanear MAC en la red", "MITM por ARP", "gratuitous ARP" o pida ayuda para configurar, depurar o entender estos scripts en un entorno de pruebas controlado. No lo utilices para atacar redes o dispositivos de terceros sin autorización.
---

# ARP Lab Toolkit

Skill de apoyo para trabajar con el repositorio [`hackingyseguridad/arp`](https://github.com/hackingyseguridad/arp), un conjunto de 7 scripts (Bash + Python/Scapy) orientados a la enseñanza de ARP Spoofing, cambio de MAC, escaneo de red y ataques MITM a nivel de capa de enlace.

## ⚠️ Condición de uso (obligatoria)

Antes de ayudar a ejecutar cualquier script de este repositorio, confirma con el usuario que el objetivo es:
- una **red de laboratorio propia** (VMs aisladas, VLAN de pruebas, entorno tipo GNS3/VirtualBox), o
- una **auditoría con autorización explícita por escrito**.

Si el contexto sugiere una red de terceros, un dispositivo ajeno o no hay autorización clara, no proporciones ayuda para ejecutar el ataque; puedes seguir explicando conceptos teóricos de ARP y detección/defensa.

## Cuándo usar esta skill

- El usuario quiere clonar, instalar dependencias o ejecutar alguno de los scripts del repo.
- Necesita depurar un error de uno de los scripts (p. ej. `mitm.py` con `raw_input` en Python 3).
- Quiere entender qué hace cada script antes de ejecutarlo.
- Necesita adaptar un script a su entorno (interfaz de red distinta, rango IP distinto).
- Quiere documentación, un README, o comparar los scripts entre sí.
- Quiere saber cómo detectar o defenderse de estas técnicas (IDS, ARPwatch, DAI, VLANs).

## Inventario de scripts

| Script | Lenguaje | Técnica | Requiere root | Interactivo |
|---|---|---|:---:|:---:|
| `arpspoof.sh` | Bash | ARP Spoofing bidireccional (usa `arpspoof` de dsniff) | Sí | No (usa argumentos) |
| `mitm.py` | Python 2 + Scapy | MITM manual (ARP reply forjado a víctima y gateway) | Sí | Sí |
| `gratuitousarp.py` | Python 2 + Scapy | Gratuitous ARP en bucle | Sí | No |
| `flood.py` | Python 2 + Scapy | ARP flood dirigido a un objetivo | Sí | Sí |
| `colpasoarp.sh` | Bash | Añade entrada ARP estática con IP aleatoria | Sí | No |
| `cambiarmac.sh` | Bash | Cambia la MAC de una interfaz (`eth0` por defecto) | Sí | No |
| `scanmac.sh` | Bash | Escanea un rango IP y lista pares IP=MAC vía `nmap -sn` | Sí | No (recibe rango como argumento) |

## Flujo de trabajo recomendado

1. **Verificar contexto y autorización** (ver sección de arriba).
2. **Instalar dependencias** según el script objetivo:
   - `arpspoof.sh` → `sudo apt-get install dsniff`
   - `scanmac.sh` → `sudo apt-get install nmap`
   - `mitm.py`, `gratuitousarp.py`, `flood.py` → Python 2 + `pip2 install scapy`
   - `cambiarmac.sh` → `net-tools` (`ifconfig`) o `iproute2` (`ip`)
3. **Adaptar variables al entorno del usuario**: nombre de interfaz (`eth0` vs `enp0s3`/`wlan0`), IPs de víctima/gateway, rango de red.
4. **Ejecutar y monitorizar**: recordar que casi todos requieren `sudo` y que algunos activan `ip_forward` (hay que revertirlo al terminar si el script no lo hace automáticamente — `gratuitousarp.py` y `flood.py` no lo restauran).
5. **Detener limpiamente**: `arpspoof.sh` restaura `ip_forward` al pulsar una tecla; los scripts en Python normalmente requieren `Ctrl+C` y no limpian el estado — avisa de esto al usuario.
6. **Documentar/objetar**: si se pide un README o resumen del repo, generar tablas y explicaciones siguiendo el patrón de este documento.

## Notas técnicas importantes a tener en cuenta al ayudar

- **`mitm.py` y `flood.py` están escritos en Python 2** (`raw_input()`, módulo `commands`, que no existen en Python 3). Si el usuario tiene solo Python 3, la opción más simple es ejecutarlos con un intérprete Python 2 instalado aparte; si pide "modernizarlos", se puede ayudar a adaptar la sintaxis (`raw_input` → `input`, `commands.getoutput` → `subprocess.check_output`) porque es una tarea de compatibilidad, no de creación de nueva capacidad ofensiva.
- **`cambiarmac.sh` y `mitm.py` tienen valores fijos** (`00:e0:4c:53:44:58`, `192.168.230.131`, etc.) que hay que editar antes de ejecutar en cualquier entorno distinto al original.
- **`colpasoarp.sh`** solo añade una entrada local (`ip neigh add`); no envía tráfico a la red, por lo que es el de menor riesgo/impacto.
- **`scanmac.sh`** es puramente de reconocimiento (no altera nada), útil como primer paso antes de cualquier otro script.

## Defensa y detección (para responder preguntas del "otro lado")

| Medida | Efecto |
|---|---|
| Dynamic ARP Inspection (DAI) en switches gestionados | Bloquea respuestas ARP no válidas |
| DHCP Snooping | Base de datos de confianza IP-MAC-puerto para validar ARP |
| ARPwatch / arpalert | Alerta ante cambios inesperados en la tabla ARP |
| Entradas ARP estáticas en hosts críticos | Elimina la ventana de envenenamiento para ese host |
| Segmentación en VLANs | Limita el dominio de difusión y el alcance del ataque |

## Referencia

README ampliado del repositorio (generado previamente, con detalle de cada script, tablas de instalación, comparativa y contramedidas): ver `README.md` en este mismo directorio de salida si está disponible en la conversación.
