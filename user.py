import socket
from room_manager import RoomManager


class User:
    def __init__(self, connection: socket.socket, name: str):
        self.connection = connection
        self.name = name
        print("New user created, nickname: {0}.".format(name))

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

    def recv(self, buffer=4096) -> str:
        """해당 유저에게서 데이터를 받아온다.

        Parameter:
            buffer: int
                선택적. 한번에 데이터를 받아올 버퍼의 양을 지정하는 정수

        Return:
            str
                유저에게 받아온 데이터를 문자열로 변환 후 리턴
        """
        return self.connection.recv(buffer).decode().strip()
