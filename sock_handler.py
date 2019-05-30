import json
from socketserver import BaseRequestHandler

import response_template
from room_manager import Room, RoomManager
from user import User


retry = {
    "msgType": "rspAnswerCorrect",
    "Data": {
        "reqResult": False,
        "msg": "Not correct answer."
    }
}

user_ids = []


def logging(msg, data):
    if data:
        print("{0}: {1}".format(msg, data))
    else:
        print("{0}".format(msg))


class SockHandler(BaseRequestHandler):
    def handle(self):
        self.null_count = 0

        # hand shake start
        while self.null_count < 5:
            msg = self.request.recv(1024).decode().strip()
            logging("Get Message", msg)

            method, datas = self.processing_message(msg)

            if method == "reqLogin":
                name = datas["userId"]

                if name not in user_ids:
                    self.user = User(self.request, name)
                    user_ids.append(name)
                    self.request.send(bytes(json.dumps(
                        response_template.basic("rspLogin", True)), "UTF-8")
                    )
                    logging("User login success with name", str(self.user))
                    break
                else:
                    self.request.send(bytes(json.dumps(
                        response_template.basic(
                            "rspLogin", False, "Already ID exist.")
                    ), "UTF-8"))
                    logging("Already ID exists with name", name)
        # hand shake end

        while self.null_count < 5:
            msg = self.user.recv()
            logging("Get Message from {0}".format(str(self.user)), msg)

            method, datas = self.processing_message(msg)

            if method == "reqRoomList":
                self.user.send(RoomManager().get_room_infomation())

            elif method == "reqEntranceRoom":
                room_id = datas["roomId"]

                if RoomManager().check_room_is_exist(room_id):
                    self.user.send(RoomManager().join_room(room_id, self.user))

                    if RoomManager().find_room(room_id).is_full():
                        RoomManager().start_game(room_id)
                else:
                    logging("Room is not exists", room_id)

            elif method == "reqRoomMake":
                self.user.send(
                    RoomManager().new_rooms(
                        datas["name"],
                        self.user,
                        datas["content"],
                        datas["subject"]
                    )
                )

            elif method == "reqRoomExit":
                room = self.user.room

                self.user.send(RoomManager().exit_room(room, self.user))

                if room.is_empty():
                    RoomManager().remove_room(room)

            elif method == "reqTouchEvent":
                room = self.user.room
                room.draw(datas["Event"], datas["Pen"], self.user)

            elif method == "reqAnswerCorrect":
                room = self.user.room

                if not self.user == room.tagger:
                    self.user.send(
                        response_template.basic(
                            "rspAnswerCorrect",
                            False,
                            "You are not a tagger."
                        )
                    )
                    continue

                elif not room.now_turn == -1:
                    self.user.send(
                        response_template.basic(
                            "rspAnswerCorrect",
                            False,
                            "It's not tagger's turn."
                        )
                    )
                    continue

                if room.keyword == datas["answer"]:
                    room.end_game(True)
                else:
                    room.end_game(False)

                # if int(datas["attempt"]) > 3:
                #     room.end_game(False)
                # elif room.keyword == datas["answer"]:
                #     room.end_game(True)
                # else:
                #     self.user.send(
                #         response_template.basic(
                #             "rspAnswerCorrect",
                #             False
                #         )
                #     )

        try:
            user_ids.remove(self.user)
            del self.user
        except (AttributeError, ValueError):
            pass

    def processing_message(self, message):
        try:
            msg = json.loads(message)
            self.null_count = 0
            return msg["msgType"], msg["Data"]
        except (TypeError, json.decoder.JSONDecodeError):
            logging(
                "Passed null method",
                "{0} times left".format(5 - self.null_count)
            )
            self.null_count += 1
            return None, None
