from HellMusic import SUDO_USERS


on_mode = ["on", "yes", "enable", "true"]


async def check_mode(message):
    mode = Config.PRIVATE_MODE
    if mode.lower() in on_mode:
        user = message.from_user.id
        if user in SUDO_USERS:
            return 1
        else:
            return 0
