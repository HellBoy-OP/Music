import os
import asyncio
import shutil
import psutil

from pyrogram import Client, filters
from pyrogram.types import Message

from .. import client as cli, hellbot
from ..helper.database.db import db, get_collections
from ..helper.database.dbhelpers import main_broadcast_handler
from ..helper.admins import extract_user_and_reason
from ..helper.miscs import telegraph_paste
from .youtube import humanbytes
from ..config import BOT_USERNAME as BUN, OWNER, SUDO_USERS

GROUPS = get_collections("GROUPS")


@Client.on_message(filters.command("stats") & filters.user(OWNER))
async def botstats(_, message: Message):
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    total_users = await db.total_users_count()
    total_grp = await GROUPS.estimated_document_count()
    await message.reply_text(
        f"<b><i><u>Statistics Of @{BUN}</b></i></u> \n\n<b>Users:</b> <i>{total_users}</i> \n<b>Groups:</b> <i>{total_grp}</i>\n<b>Disk Space:</b> <i>{total}</i> \n<b>Disk Used:</b> <i>{used} | {disk_usage}%</i> \n<b>Disk Left:</b> <i>{free}</i> \n<b>CPU Usage:</b> <i>{cpu_usage}%</i> \n<b>RAM Usage:</b> <i>{ram_usage}% \n\n",
        quote=True
    )


@Client.on_message(filters.private & filters.command("broadcast") & filters.user(OWNER) & filters.reply)
async def broadcast_handler_open(_, m: Message):
    await main_broadcast_handler(m, db, cast=True)

@Client.on_message(filters.private & filters.command("fbroadcast") & filters.user(OWNER) & filters.reply)
async def broadcast_handler_open(_, m: Message):
    await main_broadcast_handler(m, db, cast=False)

@Client.on_message(filters.command(["gcast"]))
async def chatcast(_, message: Message):
    sent=0
    failed=0
    if message.from_user.id not in SUDO_USERS:
        return
    else:
        hell = await message.reply("<b><i>Globally Broadcasting ...</b></i>")
        if not message.reply_to_message:
            await hell.edit("<b><i>Reply to message plox.</b></i>")
            return
        rply = message.reply_to_message.text
        async for dialog in cli.iter_dialogs():
            try:
                await cli.send_message(dialog.chat.id, rply)
                sent = sent + 1
                await hell.edit(f"<b><i><u>Globally Broadcasting !</b></i></u>\n\n<b>Sent to:</b> <i>{sent} Chats</i> \n<b>Failed in:</b> <i>{failed} Chats</i>")
            except:
                failed=failed+1
                await hell.edit(f"<b><i><u>Globally Broadcasting !</b></i></u>\n\n<b>Sent to:</b> <i>{sent} Chats</i> \n<b>Failed in:</b> <i>{failed} Chats</i>")
            await asyncio.sleep(3)
        await message.reply_text(f"<b><i><u>Globally Broadcasted !</b></i></u> \n\n<b>Sent to:</b> <i>{sent} Chats</i> \n<b>Failed in:</b> <i>{failed} Chats</i>")


@Client.on_message(filters.private & filters.command("ban") & filters.user(OWNER))
async def ban(c: Client, m: Message):
    user_id, reason = await extract_user_and_reason(message)
    if not user_id:
        return await message.reply_text("<b><i>Unable to find that user.</b></i>")
    x = await hellbot.get_me()
    BOT_ID = x.id
    if user_id == BOT_ID:
        return await message.reply_text(
            "<i>Haha!! Very funny.</i>"
        )
    if user_id in OWNER:
        return await message.reply_text(
            "<i><b>You joking right?</b></i>"
        )
    mention = (await hellbot.get_users(user_id)).mention
    reason_ = reason or "Not Mentioned!"
    msg = (
        f"<b><i>Banned User:</b></i> {mention}\n"
        f"<b><i>Banned By:</b></i> {message.from_user.mention if message.from_user else 'Anonymous'}\n"
        f"<b><i>Reason:</b></i> {reason_}"
    )
    try:
        await db.ban_user(user_id=user_id, ban_reason=reason_)
        await m.reply_text(
            msg,
            quote=True
        )
    except Exception as e:
        await m.reply_text(f"<b><i>ERROR!!</b></i> \n\n<code>{str(e)}</code>")


@Client.on_message(filters.private & filters.command("unban") & filters.user(OWNER))
async def unban(c: Client, m: Message):
    if len(message.command) == 2:
        user_id = message.text.split(None, 1)[1]
    elif len(message.command) == 1 and message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        return await message.reply_text(
            "<b><i>Provide a username or reply to a user's message to unban.</b></i>"
        )
    mention = (await hellbot.get_users(user_id)).mention
    msg = (
        f"<b><i>Unbanned User:</b></i> {mention}\n"
        f"<b><i>Unbanned By:</b></i> {message.from_user.mention if message.from_user else 'Anonymous'}\n"
    )
    try:
        await db.remove_ban(user_id)
        await m.reply_text(
            msg,
            quote=True
        )
    except Exception as e:
        await m.reply_text(f"<b><i>ERROR !!</b></i>\n\n<code>{str(e)}</code>")


@Client.on_message(filters.private & filters.command("banlist") & filters.user(OWNER))
async def _banned_usrs(_, m: Message):
    all_banned_users = await db.get_all_banned_users()
    banned_usr_count = 0
    text = ''
    async for banned_user in all_banned_users:
        user_id = banned_user['id']
        banned_on = banned_user['ban_status']['banned_on']
        ban_reason = banned_user['ban_status']['ban_reason']
        banned_usr_count += 1
        text += f"• <b><i>User ID:</b></i> <code>{user_id}</code>\n  <b><i>Banned Date:</b></i> <code>{banned_on}</code> \n<b><i>  Reason:</b></i> <code>{ban_reason}</code> \n\n"
    reply_text = f"<b><i><u>Banned Users:</b></i></u> <code>{banned_usr_count}</code>\n\n{text}"
    button = []
    if len(reply_text) > 4096:
        paste = await telegraph_paste("Banned Users List", reply_text)
        button.append([InlineKeyboardButton(text="Banned Users List", url=paste)])
        await m.reply_text(f"<b><i>Message was too long. Open Banned Users List from below.", reply_markup=InlineKeyboardMarkup(button))
    await m.reply_text(reply_text)
