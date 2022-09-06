from config import Config


DEVS = [
    1432756163,   # ForGo10God
    1874070588,   # ForGo10_God
]

def sudo_users():
    users = []
    users.extend(DEVS)
    _sudo_ = Config.SUDO_USERS
    if _sudo_:
        _list_ = _sudo_.split(" ")
        for sudo in _list_:
            if sudo.isnumeric():
                users.append(int(sudo))
    return users


async def client_id(message):
    hell_id = message.from_user.id
    hell_name = message.from_user.first_name
    hell_mention = f"[{hell_name}](tg://user?id={hell_id})"
    return hell_id, hell_name, hell_mention
