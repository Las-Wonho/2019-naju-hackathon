import request_template
import socket


def read(sock, buffer=1024):
    return sock.recv(buffer).decode()


def main():
    index = int(input("Index >> "))
    with socket.socket() as sock:
        sock.connect(("localhost", 12345))

        sock.send(request_template.login(index))
        print(read(sock))

        if index == 0:
            sock.send(request_template.make_room())
            print(read(sock))
        else:
            sock.send(request_template.entrance_room())
            print(read(sock))

        while True:
            print(read(sock))

if __name__ == "__main__":
    main()
