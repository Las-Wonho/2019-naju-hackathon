import json
from socketserver import BaseRequestHandler

from room_manager import Room, RoomManager
from user import User


response_template = {
    "msgType": "rspLogin",
    "Data": {
        "reqResult": True,
        "msg": ""
    }
}

user_ids = []


class SockHandler(BaseRequestHandler):
    def handle(self):
        self.null_count = 0

        # hand shake start
        while self.null_count < 10:
            msg = self.request.recv(1024).decode().strip()
            print("Get Message:", msg)

            method, datas = self.processing_message(msg)
            response = response_template

            if method == "reqLogin":
                name = datas["userId"]

                if name not in user_ids:
                    response["Data"]["reqResult"] = True
                    response["Data"]["msg"] = ""

                    self.user = User(self.request, name)
                    user_ids.append(name)
                    self.request.send(bytes(json.dumps(response), "UTF-8"))
                    break
                else:
                    response["Data"]["reqResult"] = False
                    response["Data"]["msg"] = "Already ID exist."

                    self.request.send(bytes(json.dumps(response), "UTF-8"))
            elif method is None:
                print("Passed null value")
                continue
        # hand shake end
        print("Break First For Loop")

        while self.null_count < 10:
            msg = self.user.recv()
            print("Get Message:", msg)
            method, datas = self.processing_message(msg)

            if method == "reqRoomList":
                self.user.send(
                    json.dumps(
                        RoomManager().get_room_infomation()
                    )
                )
            elif method == "reqEntranceRoom":
                room_id = datas["roomId"]

                if RoomManager().check_room_is_exist(room_id):
                    self.user.send(
                        json.dumps(
                            RoomManager().join_room(datas["roomId"], self.user)
                        )
                    )
                    if RoomManager().find_room(room_id).is_full():
                        RoomManager().start_game(room_id)
            elif method == "reqExitRoom":
                pass
            elif method is None:
                continue
        print("Break Second For Loop")

        self.request.close()

    def processing_message(self, message):
        try:
            response = json.loads(message)["msgType"], json.loads(message)["Data"]
            self.null_count = 0
            return response
        except json.decoder.JSONDecodeError:
            self.null_count += 1
            return None, None
