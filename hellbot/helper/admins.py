from typing import List, Dict, Union
from pyrogram.types import Chat, User, Message

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
        return await get_admins(chat)


async def extract_userid(message, text: str):
    def is_int(text: str):
        try:
            int(text)
        except ValueError:
            return False
        return True
    text = text.strip()
    if is_int(text):
        return int(text)
    entities = message.entities
    app = message._client
    if len(entities) < 2:
        return (await app.get_users(text)).id
    entity = entities[1]
    if entity.type == "mention":
        return (await app.get_users(text)).id
    if entity.type == "text_mention":
        return entity.user.id
    return None


async def extract_user_and_reason(message):
    args = message.text.strip().split()
    text = message.text
    user = None
    reason = None
    if message.reply_to_message:
        reply = message.reply_to_message
        if not reply.from_user:
            return None, None
        if len(args) < 2:
            reason = None
        else:
            reason = text.split(None, 1)[1]
        return reply.from_user.id, reason
    if len(args) == 2:
        user = text.split(None, 1)[1]
        return await extract_userid(message, user), None
    if len(args) > 2:
        user, reason = text.split(None, 2)[1:]
        return await extract_userid(message, user), reason
    return user, reason


async def extract_user(message):
    return (await extract_user_and_reason(message))[0]
