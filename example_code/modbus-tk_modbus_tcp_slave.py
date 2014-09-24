import modbus_tk
import modbus_tk.modbus_tcp as modbus_tcp
import threading
import modbus_tk.defines as mdef
import sys
import argparse
import logging
import signal


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--level', help='defines the log level to be dispayed to the screen', default='info')
    parser.add_argument('-f', '--filename', help='defines the filename of the debugs log', default='')
    parser.add_argument('-p', '--port', help='set TCP port for modbus slave', default=502)
    args = parser.parse_args()

    # assuming args.level is bound to the string value obtained from the
    # command line argument. Convert to upper case to allow the user to
    # specify --log=DEBUG or --log=debug
    numeric_level = getattr(logging, args.level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.level)

    logger = modbus_tk.utils.create_logger(name="console", level=args.level.upper(), record_format="%(levelname)s: %(message)s")
    # logger = logging.getLogger('modbus_tk_tcp_slave')
    # # configure logger
    # # logger.setLevel(logging.DEBUG)
    # handler_stream_formatter = logging.Formatter('%(levelname)s: %(message)s')
    # handler_stream = logging.StreamHandler()
    # handler_stream.setFormatter(handler_stream_formatter)
    # handler_stream.setLevel(args.level.upper())
    # logger.addHandler(handler_stream)
    logger.debug('Log Level is: %s' % (args.level.upper()))

    # if args.filename != '':
    #     handler_file = logging.FileHandler('/home/jeastman/logs/' + args.filename)
    #     logger.debug('Log Filename is: %s' % (handler_file))
    #     handler_file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    #     handler_file.setFormatter(handler_file_formatter)
    #     # handler_file.setLevel(level.DEBUG)
    #     logger.addHandler(handler_file)
    logger.debug('Log Filename is: %s' % (args.filename))


    server = modbus_tcp.TcpServer(port=int(args.port))

    #creates a slave with id 0
    slave1 = server.add_slave(11)
    #add 2 blocks of holding registers
    slave1.add_block("a", mdef.HOLDING_REGISTERS, 100, 20)#address 0, length 100
    slave1.add_block("b", mdef.HOLDING_REGISTERS, 200, 20)#address 200, length 20

    #set the values of registers at address 0
    slave1.set_values("a", 100, range(20))

    server.start()

    while True:
        cmd = sys.stdin.readline()
        args = cmd.split(' ')

        if cmd.find('quit')==0:
            # validate_data_thread.join()
            logger.info('bye-bye...')
            server.stop()
            break
        # elif cmd.find('restart')==0:
        #     os.system('clear')

        #     # stop validate_data_thread
        #     validate_data_thread.join()

        #     # tell user restarting in 30 seconds
        #     logger.info('Restarting in %i seconds' % (30))

        #     for i in range(1, 31):
        #         if (((30 - i) % 5) == 0) and ((30 - i) != 0):
        #             logger.info('Restarting in %i seconds' % (30 - i))
        #         elif (2 <= (30 - i) <= 4):
        #             logger.info('Restarting in %i seconds' % (30 - i))
        #         elif (30 - i) == 1:
        #             logger.info('Restarting in %i second' % (30 - i))

        #         time.sleep(1)

        #     # restart validate_data_thread
        #     validate_data_thread = dataValidation()
        #     validate_data_thread.start()
        #     logger.info('Restarted...')
        # elif cmd.find('start')==0:
        #     os.system('clear')
        #     logger.info('Starting Test...')
        #     validate_data_thread.starttest()
        # elif cmd.find('stop')==0:
        #     logger.info('Stopping Test...')
        #     validate_data_thread.stoptest()
        # elif cmd.find('help')==0:
        #     sys.stdout.write('enter "start" to start the test\r\n')
        #     sys.stdout.write('enter "stop" to stop the test\r\n')
        #     sys.stdout.write('enter "restart" to restart the testing, if errors recieved\r\n')
        else:
            sys.stdout.write('unknown command %s\r\n' % (args[0]))