import json
import socket
import time


with open("test.json", "r", encoding="UTF-8") as f:
    test_data_set = json.load(f)


req_login = test_data_set["login"]
req_room_list = test_data_set["room_request"]
req_make_room = test_data_set["make_room"]
req_join_room = test_data_set["join_room"]
req_game_event = test_data_set["game_event"]
req_check = test_data_set["check_answer"]


def get_login(index):
    return json.dumps(req_login[index]).encode()


def make_room():
    return json.dumps(req_make_room).encode()


def join_room(room_id):
    req = req_join_room
    req["Data"]["roomId"] += room_id

    return json.dumps(req).encode()


def get_event(user_id, room_id):
    req = req_game_event
    req["Data"]["userId"] = user_id
    req["Data"]["roomId"] += room_id

    return json.dumps(req).encode()


def check_answer():
    req = req_check
    req["Data"]["answer"] = input("Input Answer: ")

    return json.dumps(req).encode()


def read(sock, buffer=1024):
    msg = sock.recv(buffer).decode()
    print("> {0}".format(msg))


def run():
    with socket.socket() as sock:
        sock.connect(("localhost", 12346))

        index = int(input("User ID index: "))

        sock.send(get_login(index))
        read(sock)

        yes_or_no = input("Do you want to make a room? [Y / N] >> ").upper()
        if yes_or_no == "Y":
            sock.send(make_room())
            read(sock)
        else:
            room_id = input("Room ID: ")
            sock.send(join_room(room_id))
            read(sock)

        input("Input enter to start game.")
        for i in range(3):
            print("attempts: {0}".format(i))
            sock.send(get_event(req_login[index]["Data"]["userId"], room_id))
            read(sock)
            time.sleep(1)

        sock.send(check_answer())
        read(sock)

        input("End.")


run()
