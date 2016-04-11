#include <modbus/modbus.h>
#include <modbus/modbus-rtu.h>
#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <time.h>

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

	uint16_t tab_reg[64];
	int i;
	int debug=0;

	if (argc==1)
	{
		fprintf(stderr,"Usage: %s <reg>\n", argv[0]);
		exit(1);
	}

	/* Lock file */
	srandom(time(NULL));
	i=0;
	f_lock=fopen("/var/run/modbus.lck","r");
	while (i < 4 && f_lock>0)
	{
		fclose(f_lock);
		usleep(500000*random()%10);
		i++;
		f_lock=fopen("/var/run/modbus.lck","r");
	}
	if (i==4) 
	{ 
		fprintf(stderr, "Lock timeout\n");
		exit(1);
	}
	if (f_lock<0)
	{
		f_lock=fopen("/var/run/modbus.lck","a");
		fputs("modbus",f_lock);
		fclose(f_lock);
	}

	/* Open Serial Device */
	diris=modbus_new_rtu("/dev/ttyUSB0", 9600, 'O', 8, 1);
	if (diris == NULL) {
	    fprintf(stderr, "Unable to create the libmodbus context\n");
	    unlink("/var/run/modbus.lck");
	    return 1;
	}

	/* Prepare to connect to Slave */
	code=modbus_set_slave(diris, 5);
	if(code <0)
	{
		perror(errmsg);
		fprintf(stderr,"Set slave error: %s\n",errmsg);
	    unlink("/var/run/modbus.lck");
		return 1;
	}

	if (debug)
		modbus_set_debug(diris, 1);

	if (debug)
	{
		/* Check Serial Mode */
		code=modbus_rtu_get_serial_mode(diris);
		if (code=MODBUS_RTU_RS485)
		{
			printf("Mode: RS485\n");
		}
		else
		{
			printf("Mode: RS232\n");
		}
	}

	if (debug)
	{
		/* Check RTS Mode */
		code=modbus_rtu_get_rts(diris);
		switch(code)
		{
			case MODBUS_RTU_RTS_NONE:
			printf("RTS: None\n");
			break;
			case MODBUS_RTU_RTS_UP:
			printf("RTS: Up\n");
			break;
			case MODBUS_RTU_RTS_DOWN:
			printf("RTS: Down\n");
			break;
			default:
			printf("RTS: Unknown\n");
		}
		printf("RTS: %d\n", code);
	}

	/* Change RTS Mode */
	modbus_rtu_set_rts(diris, MODBUS_RTU_RTS_UP);

	if (debug)
	{
		code=modbus_rtu_get_rts(diris);
		switch(code)
		{
			case MODBUS_RTU_RTS_NONE:
			printf("RTS: None\n");
			break;
			case MODBUS_RTU_RTS_UP:
			printf("RTS: Up\n");
			break;
			case MODBUS_RTU_RTS_DOWN:
			printf("RTS: Down\n");
			break;
			default:
			printf("RTS: Unknown\n");
		}
		printf("RTS: %d\n", code);
	}

	/* Initiate connect (nothing to do in serial mode) */
	if (modbus_connect(diris) == -1) {
	    fprintf(stderr, "Connection failed: %s\n", modbus_strerror(errno));
	    modbus_free(diris);
	    unlink("/var/run/modbus.lck");
	    return -1;
	}
	if (debug) {printf("Connect OK\n");}
	

	/* Do the read */
	if (debug) { printf("Reading %s\n", argv[1]); }
	/* int modbus_read_registers(modbus_t *ctx, int addr, int nb, uint16_t *dest); */
	code = modbus_read_registers(diris, atoi(argv[1]), 2, tab_reg);
	if (code == -1) {
	    fprintf(stderr, "%s\n", modbus_strerror(errno));
		modbus_close(diris);
		modbus_free(diris);
	    unlink("/var/run/modbus.lck");
	    return -1;
	}

	/* Display Value returned */
	/*for (i=0; i < code; i++) {
	    printf("reg[%d]=%d (0x%X)\n", i, tab_reg[i], tab_reg[i]);
	}
	*/
	if (code==2)
	{
		printf("%d\n", tab_reg[1]);
	}

	/*printf("Reset IMax\n");
	code=modbus_write_register(diris, 1024, 1);
	if (code == -1)
	{
	    fprintf(stderr, "%s\n", modbus_strerror(errno));
		modbus_close(diris);
		modbus_free(diris);
	    return -1;
	}*/

	/* Close */
	modbus_close(diris);
	modbus_free(diris);
	unlink("/var/run/modbus.lck");
	return 0;
}
