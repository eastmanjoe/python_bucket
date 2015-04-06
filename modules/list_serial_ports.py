import serial.tools.list_ports


def list_serial_ports():
    """Lists serial ports

    """

    return list(serial.tools.list_ports.comports())


if __name__ == '__main__':
    for p in list_serial_ports():
        print p