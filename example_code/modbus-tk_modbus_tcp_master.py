import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp

if __name__ == "__main__":
    try:
        #Connect to the slave
        master = modbus_tcp.TcpMaster(host='10.11.40.36', port=8502, timeout_in_sec=2.0)

        print master.execute(1, cst.READ_HOLDING_REGISTERS, 100, 3)

        # master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 100, output_value=xrange(12))

    except modbus_tk.modbus.ModbusError, e:
        print "Modbus error ", e.get_exception_code()

    except Exception, e2:
        print "Error ", str(e2)