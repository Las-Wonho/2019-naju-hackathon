import socketserver
from sys import argv

from test_handler import TestHandler
from sock_handler import SockHandler


HOST = ""
PORT = 12345

if len(argv) > 1:
    PORT = int(argv[1])


def main():
    print("Run TCP Server")

    try:
        server = socketserver.ThreadingTCPServer((HOST, PORT), SockHandler)
        print("Running on IP: {0}, Port: {1}".format(*server.server_address))
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutdown server")
        server.shutdown()

if __name__ == "__main__":
    main()
