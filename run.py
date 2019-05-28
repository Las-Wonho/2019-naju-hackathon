import socketserver

from test_handler import TestHandler


HOST = "0.0.0.0"
PORT = 12345


def main():
    print("Run TCP Server")

    try:
        server = socketserver.ThreadingTCPServer((HOST, PORT), TestHandler)
        print("Running on IP: {0}, Port: {1}".format(*server.server_address))
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stop server")
        server.shutdown()

if __name__ == "__main__":
    main()
