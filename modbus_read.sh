#!/bin/bash

SPOOL_DIR=/run/diris

if [ -z "$1" ]
then
	echo "ERREUR"
	exit 1
fi

if [ -f ${SPOOL_DIR}/$1 ]
then
	cat ${SPOOL_DIR}/$1
else
	touch ${SPOOL_DIR}/$1
fi

