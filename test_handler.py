from socketserver import BaseRequestHandler


class TestHandler(BaseRequestHandler):
    def handle(self):
        print(self.request)
        while True:
            msg = self.request.recv(1024).decode()
            print(msg)
            self.request.send(msg.encode())
            print("Send:", msg)
