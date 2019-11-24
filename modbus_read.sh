#!/bin/bash
#
# Wrapper to query Diris:
#  $1: register
#  $2: "conv"=convert value

SPOOL_DIR=/run/diris

if [ -z "$1" ]
then
	echo "ERREUR"
	exit 1
fi

if [ -f ${SPOOL_DIR}/$1 ]
then
	# Register is in the query list
    RES=`cat ${SPOOL_DIR}/$1`
	if [ -n "RES"]
	then
		# We are sure we have a value
    	if [ $RES -gt 32768 -a "$2" = "conv" ]
    	then
			# We need to convert the value
			expr $RES - 65535
		else
			echo $RES
		fi
	fi
else
	# Ask spooler to query this register
    touch ${SPOOL_DIR}/$1
fi
