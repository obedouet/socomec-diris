/*
 * Modbus reader
 * Take register in param
 */

#include <linux/serial.h>
#include <modbus/modbus.h>
#include <modbus/modbus-rtu.h>
#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#ifndef MODBUS_RTU_RTS_NONE
#define MODBUS_RTU_RTS_NONE   0
#endif
#ifndef MODBUS_RTU_RTS_UP
#define MODBUS_RTU_RTS_UP     1
#endif
#ifndef MODBUS_RTU_RTS_DOWN
#define MODBUS_RTU_RTS_DOWN   2
#endif

int main(int argc, char *argv[])
{
	modbus_t *diris;
	int code;
	char errmsg[255];
	FILE *f_lock;
	char value[12];

	uint16_t tab_reg[64];
	int i, fd;
	int debug=0;

	struct timeval old_response_timeout;
    struct timeval response_timeout;

	/*if (argc==1)
	{
		fprintf(stderr,"Usage: %s <reg>\n", argv[0]);
		exit(1);
	}*/

	if (getenv("DEBUG")!=NULL)
	{
		debug=1;
	}

	/* Lock file */
	if (debug) fprintf(stderr, "DEBUG: opening lock\n");
	srandom(time(NULL));
	i=0;
	f_lock=fopen("/var/run/modbus.lck","r");
	while (i < 4 && f_lock>0)
	{
		/* Loop until lock is free */
		fclose(f_lock);
		if (debug) fprintf(stderr, "DEBUG: lock found, sleeping\n");
		usleep(500000*random()%10);
		i++;
		if (debug) fprintf(stderr, "DEBUG: re-opening lock\n");
		f_lock=fopen("/var/run/modbus.lck","r");
	}
	if (i==4) 
	{
		/* 4 tries=cancel */ 
		fprintf(stderr, "ERROR: Lock timeout\n");
		exit(1);
	}

	/* Lock is available */
	if (f_lock<0)
	{
		if (debug) fprintf(stderr, "DEBUG: creating lock\n");
		f_lock=fopen("/var/run/modbus.lck","a");
		fputs("modbus",f_lock);
		fclose(f_lock);
	}

	/* Open Serial Device */
	if (debug) fprintf(stderr, "DEBUG: open serial dev\n");
	diris=modbus_new_rtu("/dev/ttyUSB1", 9600, 'O', 8, 1);
	if (diris == NULL) {
	    fprintf(stderr, "ERROR: Unable to create the libmodbus context\n");
	    unlink("/var/run/modbus.lck");
	    exit(1);
	}

	/* Save original timeout */
    modbus_get_response_timeout(diris, &old_response_timeout);

	/* Set Timeout */
	if (debug) fprintf(stderr, "DEBUG: set timeout\n");
	response_timeout.tv_sec = 0;   //set some default timeouts in secs
	response_timeout.tv_usec = 500000;  //set some default timeouts in usec
	modbus_set_response_timeout(diris, &response_timeout);

	/* Informational purpose */
	if (debug)
	{
		code=modbus_rtu_get_serial_mode(diris);
		fprintf(stderr, "DEBUG: Serial Mode: %d ", code);
		if (code==MODBUS_RTU_RS485) fprintf(stderr, "(RS485)\n");
		if (code==MODBUS_RTU_RS232) fprintf(stderr, "(RS232)\n");
	}

	/* UNSUPPORTED ON USB DEVICES */
	//code=modbus_rtu_set_serial_mode(diris, MODBUS_RTU_RS485);
	if(code <0)
	{
		fprintf(stderr,"ERROR: Set serial mode error code: %d\n",errno);
		perror(errmsg);
		fprintf(stderr,"ERROR: Set serial mode error msg: %s\n",errmsg);
	    unlink("/var/run/modbus.lck");
		exit(1);
	}

	/* Prepare to connect to Slave */
	if (debug) fprintf(stderr, "DEBUG: set slave mode\n");
	code=modbus_set_slave(diris, 5);
	if(code <0)
	{
		perror(errmsg);
		fprintf(stderr,"ERROR: Set slave error: %s\n",errmsg);
	    unlink("/var/run/modbus.lck");
		exit(1);
	}

	/* Change RTS Mode - UNSUPPORTED */
	//modbus_rtu_set_rts(diris, MODBUS_RTU_RTS_UP);

	/* Initiate connect (nothing to do in serial mode) */
	if (modbus_connect(diris) == -1) {
	    fprintf(stderr, "ERROR: Connection failed: %s\n", modbus_strerror(errno));
	    modbus_free(diris);
	    unlink("/var/run/modbus.lck");
	    return -1;
	}
	if (debug) {fprintf(stderr, "DEBUG: Connection OK\n");}

	/* Set RTS/CTS */
	fd = modbus_get_socket(diris);

	if (argc==1)
	{
		/* Do the read */
		if (debug) { fprintf(stderr,"DEBUG: Reading %s\n", argv[1]); }
		/* int modbus_read_registers(modbus_t *ctx, int addr, int nb, uint16_t *dest); */
		code = modbus_read_registers(diris, atoi(argv[1]), 2, tab_reg);
		if (code < 0) {
			fprintf(stderr, "ERROR: %s\n", modbus_strerror(errno));
			modbus_close(diris);
			modbus_free(diris);
			unlink("/var/run/modbus.lck");
			exit(1);
		}
		else if (code==2)
		{
			printf("%d\n", tab_reg[1]);
		}
		else
		{
			fprintf(stderr, "UNKNOWN: code=%d, value=%d\n", code, tab_reg[1]);
			if (debug)
			{
				/* Display Value returned */
				for (i=0; i < code; i++) {
					fprintf(stderr, "DEBUG: reg[%d]=%d (0x%X)\n", i, tab_reg[i], tab_reg[i]);
				}
			}
		}
	}
	else
	{
		/* Read from stdin */
		while (fgets(value, 8, stdin))
		{
			if (debug) { fprintf(stderr,"DEBUG: Reading %s\n", value); }
			code = modbus_read_registers(diris, atoi(value), 2, tab_reg);
			if (code < 0) {
				fprintf(stderr, "ERROR: %s\n", modbus_strerror(errno));
				modbus_close(diris);
				modbus_free(diris);
				unlink("/var/run/modbus.lck");
				exit(1);
			}
			else if (code==2)
			{
				/* We have a response */
				printf("%s:%d\n", value, tab_reg[1]);
			}
			else
			{
				/* Unknown response */
				fprintf(stderr, "UNKNOWN: code=%d, value=%d\n", code, tab_reg[1]);
			}
			
			
		}

	}
	

	/*printf("Reset IMax\n");
	 *code=modbus_write_register(diris, 1024, 1);
	 *if (code == -1)
	 *{
	  *   fprintf(stderr, "%s\n", modbus_strerror(errno));
	 *	modbus_close(diris);
	 *	modbus_free(diris);
	  *   return -1;
	 *}
 	 */

	/* Close */
	if (debug) fprintf(stderr, "DEBUG: closing\n");
	modbus_close(diris);
	modbus_free(diris);
	unlink("/var/run/modbus.lck");
	exit(0);
}
