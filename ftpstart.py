from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer, ThreadedFTPServer
import socket
import logging
import os

folders = []
folders.append(['film', '/mnt/dumpdrive/film'])
folders.append(['film2', '/mnt/dumpdrive2/film'])
folders.append(['done', '/mnt/dumpdrive/Done'])
folders.append(['apk', '/mnt/dumpdrive/soft/apk'])
folders.append(['music', '/mnt/dumpdrive/My Music'])
folders.append(['kodi', '/mnt'])

def main():
    # Get the value of 'PUBLIC_IP' environment variable
    key = 'PUBLIC_IP'
    value = os.getenv(key)

    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions
    for folder in folders:
        authorizer.add_user(folder[0], '1', folder[1], perm='elradfmwMT')

    # Logging
    logging.basicConfig(format='[%(asctime)s] - %(message)s', filename='/home/pi/log/ftp.log', level=logging.INFO)

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer
    local_ip = get_ip()
    logging.info("My IP address is: " + local_ip)
    #logging.info("My public IP address is: " + value)

    # Define a customized banner (string returned when client connects)
    handler.banner = "pyftpdlib based ftpd ready."

    # Specify a masquerade address and the range of ports to use for
    # passive connections.  Decomment in case you're behind a NAT.
    #handler.masquerade_address = value
    handler.passive_ports = range(59990, 60000)

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    address = ('', 2121)
    server = FTPServer(address, handler)

    # start ftp server
    server.serve_forever()

# Get local IP address for masquerading
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

if __name__ == '__main__':
    main()
