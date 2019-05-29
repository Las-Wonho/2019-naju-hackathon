import json


resource = {
    "login": [
        {
            "msgType": "reqLogin",
            "Data": {
                "userId": "user1"
            }
        },
        {
            "msgType": "reqLogin",
            "Data": {
                "userId": "user2"
            }
        },
        {
            "msgType": "reqLogin",
            "Data": {
                "userId": "user3"
            }
        },
        {
            "msgType": "reqLogin",
            "Data": {
                "userId": "user4"
            }
        }
    ],

    "make_room": {
        "msgType": "reqRoomMake",
        "Data": {
            "name": "test_room",
            "content": "It is desc",
            "subject": "선생님"
        }
    },

    "entrance_room": {
        "msgType": "reqEntranceRoom",
        "Data": {
            "roomId": "test_room"
        }
    }
}


def dict_to_string(func):
    def wrapper(*args):
        return json.dumps(func(*args)).encode()
    return wrapper


@dict_to_string
def login(index):
    return resource["login"][index]


@dict_to_string
def make_room():
    return resource["make_room"]


@dict_to_string
def entrance_room():
    return resource["entrance_room"]
