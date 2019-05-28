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

                ##########################################
                # 여기서 방 검사를 했던 이유가 뭐였더라???? #
                ##########################################
                if RoomManager().check_room_is_exist(room_id):
                    self.user.send(
                        json.dumps(
                            RoomManager().join_room(datas["roomId"], self.user)
                        )
                    )
                    if RoomManager().find_room(room_id).is_full():
                        RoomManager().start_game(room_id)
            elif method == "reqRoomMake":
                self.user.send(
                    json.dumps(
                        RoomManager().new_rooms(
                            datas["name"],
                            self.user,
                            datas["content"],
                            datas["subject"]
                        )
                    )
                )
            elif method == "reqRoomExit":
                ##################################
                # 여기서도 방 검사를 해야하나????? #
                ##################################
                room_id = datas["roomId"]

                self.user.send(
                    json.dumps(
                        RoomManager().exit_room(room_id, self.user)
                    )
                )
                if RoomManager().find_room(room_id).is_empty():
                    RoomManager().remove_room(room_id)
            elif method is None:
                continue
        print("Break Second For Loop")

        print("{0} disconnected from server".format(self.user.name))
        self.request.close()

    def processing_message(self, message):
        try:
            msg = json.loads(message)
            response = msg["msgType"], msg["Data"]
            self.null_count = 0
            return response
        except json.decoder.JSONDecodeError:
            self.null_count += 1
            return None, None
