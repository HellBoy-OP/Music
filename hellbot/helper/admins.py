from typing import List, Dict, Union
from pyrogram.types import Chat, User

admins: Dict[int, List[int]] = {}

def set_ad(chat_id: int, admins_: List[int]):
    admins[chat_id] = admins_

def get_ad(chat_id: int) -> Union[List[int], bool]:
    if chat_id in admins:
        return admins[chat_id]
    return False


async def get_admins(chat: Chat) -> List[User]:
    get = get_ad(chat.id)
    if get:
        return get
    else:
        administrators = await chat.get_members(filter="administrators")
        to_set = []
        for administrator in administrators:
            if administrator.can_manage_voice_chats:
                to_set.append(administrator.user.id)

        set_ad(chat.id, to_set)
        return await get_administrators(chat)
