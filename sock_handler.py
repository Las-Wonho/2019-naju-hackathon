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
retry = {
    "msgType": "rspAnswerCorrect",
    "Data": {
        "reqResult": False,
        "msg": "Not correct answer."
    }
}
user_ids = []


class SockHandler(BaseRequestHandler):
    def handle(self):
        self.null_count = 0

        # hand shake start
        while self.null_count < 10:
            try:
                msg = self.request.recv(1024).decode().strip()
            except ConnectionResetError:
                print(
                    "{0} shutdown during server recieves messages."
                    .format(self.user.name)
                )
                return
            print("Get Message:", msg, end="\n\n")

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
            print("Get Message:", msg, end="\n\n")
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
                            RoomManager().join_room(room_id, self.user)
                        )
                    )
                    if RoomManager().find_room(room_id).is_full():
                        RoomManager().start_game(room_id)
                else:
                    print("{0} room is not exists.".format(room_id))
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
                room_id = datas["roomId"]
                self.user.send(
                    json.dumps(
                        RoomManager().exit_room(room_id, self.user)
                    )
                )
                if RoomManager().find_room(room_id).is_empty():
                    RoomManager().remove_room(room_id)
            elif method == "reqTouchEvent":
                room = RoomManager().find_room(room_id)
                room.draw(datas["Event"], datas["Pen"], self.user)
            elif method == "reqAnswerCorrect":
                room = RoomManager().find_room(room_id)
                if int(datas["attempt"]) > 3:
                    room.end_game(False)
                elif room.keyword == datas["answer"]:
                    room.end_game(True)
                else:
                    self.user.send(retry)
            elif method is None:
                continue
        print("Break Second For Loop")
        del self.user

    def processing_message(self, message):
        try:
            msg = json.loads(message)
            response = msg["msgType"], msg["Data"]
            self.null_count = 0
            return response
        except (TypeError, json.decoder.JSONDecodeError):
            self.null_count += 1
            return None, None
