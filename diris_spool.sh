#!/bin/bash

SPOOL_DIR=/run/diris
MODBUS_READ=/home/pi/Socomec/modbus_read

cd ${SPOOL_DIR}
while [ 1 ]
do
    ls | tr -s ' ' '\n' | $MODBUS_READ | while read RESULT
    do
        echo "MODBUS:$RESULT"
        REGISTER=`echo $RESULT | awk -F: '{print $1}'`
        VALUE=`echo $RESULT | awk -F: '{print $2}'`
        if [ -n "$VALUE" -a -n "$REGISTER" ]
        then
            echo $VALUE > $REGISTER
        fi
    done
    sleep 5

done