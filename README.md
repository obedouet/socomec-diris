# modbus reader for Socomec Diris

Here is a set of tools to read data from a Socomec's Diris circuit metering with a RS485/Modbus unit

## Requisites
 - Socomec Diris (tested on A21) with Modbus option
 - Modbus USB device
 - libmodbus

## How it work

The script modbus_spool.sh is reading every 20 second data from Diris.
It takes data from /run/diris dir : file name indicate which value to ask from Diris
and store the result into the file.

## Build



## Install

At start (rc.local) you need to:
mkdir /run/diris
mkdir /run/diris_max
chown pi /run/diris
chown pi /run/diris_max

The spool is to avoid having multiple access at same time to /dev/ttyUSB0.
diris_max record the top value on 5 minute-period.

This script was tested on a Raspberry Pi B.


