async def client_id(message):
    hell_id = message.from_user.id
    hell_name = message.from_user.first_name
    hell_mention = f"[{hell_name}](tg://user?id={hell_id})"
    return hell_id, hell_name, hell_mention
