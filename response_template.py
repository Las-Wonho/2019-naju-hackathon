resource = {
    "basic": {
        "msgType": "",
        "Data": {
            "reqResult": None,
            "msg": ""
        }
    },

    "room_information": {
        "msgType": "",
        "Data": {
            "reqResult": None,
            "roomList": []
        }
    },

    "after_create_room": {
        "msgType": "",
        "Data": {
            "reqResult": None,
            "name": "",
            "content": ""
        }
    },

    "permission": {
        "msgType": "",
        "Data": {
            "observe": None,
            "draw": None
        }
    },

    "alert_start_game": {
        "msgType": "",
        "Data": {
            "reqResult": None,
            "roomId": "",
            "turn": -1,
            "subject": "",
            "keyword": "",
            "tagger": ""
        }
    }
}


def basic(msg_type, req_result, msg=""):
    basic = resource["basic"]

    basic["msgType"] = msg_type
    basic["Data"]["reqResult"] = req_result
    basic["Data"]["msg"] = msg

    return basic


def room_info(msg_type, req_result, room_list):
    room_information = resource["room_information"]

    room_information["msgType"] = msg_type
    room_information["Data"]["reqResult"] = req_result
    room_information["Data"]["roomList"] = room_list

    return room_information


def after_create(msg_type, req_result, name, content):
    after_create_room = resource["after_create_room"]

    after_create_room["msgType"] = msg_type
    after_create_room["Data"]["reqResult"] = req_result
    after_create_room["Data"]["name"] = name
    after_create_room["Data"]["content"] = content

    return after_create_room


def get_permission(msg_type, req_result, observe, draw):
    permission = resource["permission"]

    permission["msgType"] = msg_type
    permission["Data"]["observe"] = observe
    permission["Data"]["draw"] = draw

    return permission


def start_game(msg_type, req_result, *data):
    alert_start_game = resource["alert_start_game"]
    room_id, subject, keyword, tagger = data

    alert_start_game["msgType"] = msg_type
    alert_start_game["Data"]["reqResult"] = req_result
    alert_start_game["Data"]["roomId"] = room_id
    alert_start_game["Data"]["subject"] = subject
    alert_start_game["Data"]["keyword"] = keyword
    alert_start_game["Data"]["tagger"] = tagger

    return alert_start_game
