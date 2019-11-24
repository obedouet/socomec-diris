#!/bin/bash

SPOOL_DIR=/run/diris
MODBUS_READ=/home/pi/Socomec/modbus_read

cd ${SPOOL_DIR}
while [ 1 ]
do
    ls | tr -s ' ' '\n' | $MODBUS_READ | while read RESULT
    do
        REGISTER=`echo $RESULT | awk -F: '{print $1}'`
        VALUE=`echo $RESULT | awk -F: '{print $2}'`
        [ -n "$VALUE" ] && echo $VALUE > $REGISTER
    done

done