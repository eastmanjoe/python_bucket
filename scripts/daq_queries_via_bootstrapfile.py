from pymodbus.client.sync import ModbusSerialClient as ModbusClient

#---------------------------------------------------------------------------#
def setupLogger(loglevel, logfilename):
    # assuming loglevel is bound to the string value obtained from the
    # command line argument. Convert to upper case to allow the user to
    # specify --log=DEBUG or --log=debug
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    # configure logger
    # logger.setLevel(loglevel.upper())
    # handler_stream_formatter = logging.Formatter('%(levelname)s: %(message)s')
    # handler_stream = logging.StreamHandler()
    # handler_stream.setFormatter(handler_stream_formatter)
    # handler_stream.setLevel(loglevel.upper())
    # logger.addHandler(handler_stream)

    if logfilename != '':
        handler_file = logging.FileHandler('c:\\temp\\' + logfilename)
        # handler_file = logging.FileHandler('/home/jeastman/logs/' + logfilename)
        handler_file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        handler_file.setFormatter(handler_file_formatter)
        handler_file.setLevel(loglevel.upper())
        logger.addHandler(handler_file)

    logger.info('Log Level is: %s' % (loglevel))
    logger.info('Log Filename is: %s' % (logfilename))
#---------------------------------------------------------------------------#


#---------------------------------------------------------------------------#
def pa
#---------------------------------------------------------------------------#


#---------------------------------------------------------------------------#
# configure the client logging
#---------------------------------------------------------------------------#
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

for port in ['/dev/ttyxuart3']:
    client = ModbusClient(method='rtu', port=port, baudrate=9600, timeout=1, retries=1)
    client.connect()
    try:
        for addr in [3,10]:
        # for addr in xrange(10,15):
            print ('Meter Modbus Address: %d' % addr)
            # regs = client.read_holding_registers(768,120,unit=addr); print regs.registers if regs else None
            # regs = client.read_holding_registers(128,4,unit=addr); print regs.registers if regs else None
            regs = client.read_holding_registers(142,8,unit=addr); print regs.registers if regs else None

        for addr in xrange(5,9):
            print ('Inverter Modbus Address: %d' % addr)
            regs = client.read_holding_registers(33,10,unit=addr); print regs.registers if regs else None

    except AttributeError, e:
    	print 'Device not responding'
    finally:
	    client.close()

if __name__ == '__main__':

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--timeout', help='define the Modbus timeout setting', default=1)
    parser.add_argument('-r', 'retries', help='define the Modbus retries setting', default=1)
    parser.add_argument('-bf', '--bootstrap_file', help='define the bootstrap file', default='/data/daq-config.ia')
    parser.add_argument('-l', '--level', help='defines the log level to be dispayed to the screen', default='info')
    parser.add_argument('-f', '--filename', help='defines the filename of the debugs log', default='')
    args = parser.parse_args()

    # setupLogger('debug', 'modbus_log.log')
    setupLogger(args.level, args.filename)

    # parse the bootstrap file
    parseBootstrapFile(args.bootstrap_file)