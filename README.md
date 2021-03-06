# modbus reader for Socomec Diris

Here is a set of tools to read data from a Socomec's Diris circuit metering with a RS485/Modbus unit

## Requisites
 - Socomec Diris (tested on A21) with Modbus option
 - Modbus USB device
 - libmodbus
 - API: Python3, Flask

## How it work

The script modbus_spool.sh is reading every 20 second data from Diris.
It takes data from /run/diris dir : file name indicate which value to ask from Diris
and store the result into the file.

The script diris_spool.sh is an alternative: it read all entries from /run/diris and ask them at once to modbus_read. It's more efficient because it ask at once all register on Diris.

For both, register is a file in /run/diris and value is stored in. So if you create an empty file /run/diris/50524, it will ask Diris register 50524 and store the value in file. So you have a asynchronous way of querying Diris from a Cacti script. This is the purpose of modbus_read.sh: ask a register, it will create the file and manage conversion if needed (some value are signed).

Option added 12/2019: a Python-Flask based API, to simplify query by using curl instead of ssh.

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

Update: max values are suspended, will be re-enabled next

## Run

From current directory:
```
screen sh modbus_spool.sh
```

For API:
```
cd api
screen python3 main.py
``` 

This script was tested on a Raspberry Pi B.

## API CALLS

Default listen on port 5002 on all interfaces

```
/total/real : total real power in Watts
/total/apparent : total apparent power in VA
/phase1/frequency : in cents of Hz
/phase1/voltage : in volts
/phase1/amps : in mA
/phase1/apparent : apparent power in VA
/phase1/reactive : reactive power in VAR
/phase1/real : real power in Watts
/phase1/pf : Power Factor
/phase2/voltage : in volts
/phase2/amps : in mA
/phase2/apparent : apparent power in VA
/phase2/reactive : reactive power in VAR
/phase2/real : real power in Watts
/phase2/pf : Power Factor
/phase3/voltage : in volts
/phase3/amps : in mA
/phase3/apparent : apparent power in VA
/phase3/reactive : reactive power in VAR
/phase3/real : real power in Watts
/phase3/pf : Power Factor
/neutral/amps : in mA
```

Real Power is signed, as it can be negative.
Power Factor need to be converted, if value is over 32768, you have to do "65535 - value" to find the real value.


