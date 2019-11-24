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

The script diris_spool.sh is an alternative: it read all entries from /run/diris and ask them at once to modbus_read. It's more efficient because it ask at once all register on Diris.

For both, register is a file in /run/diris and value is stored in. So if you create an empty file /run/diris/50524, it will ask Diris register 50524 and store the value in file. So you have a asynchronous way of querying Diris from a Cacti script. This is the purpose of modbus_read.sh: ask a register, it will create the file and manage conversion if needed (some value are signed).

## Build

With gcc:
```
gcc -O modbus_read -o modbus_read.c -lmodbus
```

## Install

At start (rc.local) you need to:
```
mkdir /run/diris
mkdir /run/diris_max
chown pi /run/diris
chown pi /run/diris_max
```

The spool is to avoid having multiple access at same time to /dev/ttyUSB0.
diris_max record the top value on 5 minute-period.

This script was tested on a Raspberry Pi B.


