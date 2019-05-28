import socket


class User:
    def __init__(self, connection, name):
        self.connection = connection
        self.name = name
        self.room = None

    def send(self, msg) -> int:
        """해당 유저에게 메시지를 바이트 형태로 바꿔 보낸다.

        Parameter:
            msg: bytes, str, ...
                bytes 또는 문자열 또는 str() 함수를 지원하는 자료형

        Return:
            int
                유저에게 전달한 메시지의 바이트 수
        """
        if isinstance(msg, bytes):
            return self.connection.send(msg)
        elif isinstance(msg, str):
            return self.connection.send(msg.encode())
        else:
            return self.connection.send(str(msg).encode())

    def recv(self):
        
