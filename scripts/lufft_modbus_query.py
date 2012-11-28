#Lufft Modbus Query


import serial
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import logging

logger = modbus_tk.utils.create_logger("console")

if __name__ == "__main__":
    try:
        #Connect to the slave
        master = modbus_rtu.RtuMaster(serial.Serial(port=5, baudrate=19200, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        master.set_timeout(5.0)
        master.set_verbose(True)
        logger.info("connected")
        
        logger.info(master.execute(245, cst.READ_INPUT_REGISTERS, 0, 50))
        
    except modbus_tk.modbus.ModbusError, e:
        logger.error("%s- Code=%d" % (e, e.get_exception_code()))