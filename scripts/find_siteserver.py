import socket

PORT = 59990


def find_siteserver():
    # bind to address listening for siteserver response
    s_bcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_bcast.bind(('', 0))
    s_bcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s_bcast.settimeout(5)

    s_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_recv.bind(('', PORT + 2))
    s_recv.settimeout(5)

    while True:
        print "Locating siteservers..."
        s_bcast.sendto('MARCO', ('<broadcast>', PORT + 1))

        try:
            message, address = s_recv.recvfrom(1024)
        except:
            message, address = None, None

        if message:
            #print "Siteserver Replied from...", address

            return address[0]

print find_siteserver()
