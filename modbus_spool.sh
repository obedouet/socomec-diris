#!/bin/bash

SPOOL_DIR=/run/diris

IT=0
cd ${SPOOL_DIR} 
while [ 1 ]
do
	ls | while read FICH
	do
		[ -n "$FICH" ] && /home/pi/Socomec/modbus_reader $FICH > $FICH

		if [ $IT -eq 0 ]
		then
			cp $FICH /run/diris_max
		else
			OLD=`cat /run/diris_max/$FICH`
			NEW=`cat $FICH`
			if [ $NEW -gt $OLD ]
			then
				cp $FICH /run/diris_max
			fi
		fi
	done

	sleep 20

	IT=`expr $IT + 1`
	if [ $IT -gt 14 ]
	then
		IT=0
	fi
done
