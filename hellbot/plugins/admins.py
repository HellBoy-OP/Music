import asyncio
import traceback

from asyncio import QueueEmpty
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery

from .. import hellbot, client
from ..helper import pycalls, queue
from ..helper.filters import command
from ..helper.decorators import errors, authorized_users_only
from ..helper.database.db import db, mdb_, Database, get_collections
from ..helper.database.dbhelpers import handle_user_status, delcmd_is_on, delcmd_on, delcmd_off
from ..helper.miscs import clog
from ..config import BOT_USERNAME as BUN, OWNER, SUDO_USERS
from . import que, admins as admins_dict
from .callbacks import admin_check

GROUPS = get_collections("GROUPS")

@hellbot.on_message()
async def _(bot: hellbot, cmd: Message):
    await handle_user_status(bot, cmd)


BACK_BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Back ⬅️", callback_data="cbback")
        ]
    ]
)


async def delcmd(_, message: Message):
    if await delcmd_is_on(message.chat.id) and message.text.startswith("/"):
        await message.delete()
    await message.continue_propagation()



@hellbot.on_message(filters.command(["reload", "admincache", f"reload@{BUN}", f"admincache@{BUN}"]))
@authorized_users_only
async def update_admin(client: hellbot, message: Message):
    gid = message.chat.id
    gidtype = message.chat.type
    if gidtype in ["supergroup", "group"] and not await (GROUPS.find_one({"id": gid})):
        try:
            gidtitle = message.chat.username
        except KeyError:
            gidtitle = message.chat.title
        await GROUPS.insert_one({"id": gid, "grp": gidtitle})
        await clog("HELLBOT_MUSIC", f"Bot added to a new group\n\n{gidtitle}\nID: `{gid}`", "NEW_GROUP")
    global admins_dict
    admins = await client.get_chat_members(message.chat.id, filter="administrators")
    new_ads = []
    for u in admins:
        new_ads.append(u.user.id)
    for su in SUDO_USERS:
        new_ads.append(su)
    new_ads.append(OWNER)
    admins_dict[message.chat.id] = new_ads
    await message.reply_text(f"**Admins List Refreshed !!**")
 
 
@hellbot.on_message(command(["control", f"control@{BUN}"]))
@errors
@authorized_users_only
async def controlset(_, message: Message):
    gid = message.chat.id
    gidtype = message.chat.type
    if gidtype in ["supergroup", "group"] and not await (GROUPS.find_one({"id": gid})):
        try:
            gidtitle = message.chat.username
        except KeyError:
            gidtitle = message.chat.title
        await GROUPS.insert_one({"id": gid, "grp": gidtitle})
        await clog("HELLBOT_MUSIC", f"Bot added to a new group\n\n{gidtitle}\nID: `{gid}`", "NEW_GROUP")
    await message.reply_text(
        "**🕹️ Control Panel :**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Pause ⏸", callback_data="cbpause"),
                    InlineKeyboardButton("Resume ▶️", callback_data="cbresume")
                ],
                [
                    InlineKeyboardButton("Skip ⏩", callback_data="cbskip"),
                    InlineKeyboardButton("End ⏹", callback_data="cbend")
                ],
                [
                    InlineKeyboardButton("Mute 🔇", callback_data="cbmute"),
                    InlineKeyboardButton("Unmute 🔊", callback_data="cbunmute")
                ],
                [
                    InlineKeyboardButton("Close 🗑️", callback_data="close")
                ]
            ]
        )
    )



@hellbot.on_message(command(["pause", f"pause@{BUN}"]))
@errors
@authorized_users_only
async def pause(_, message: Message):
    gid = message.chat.id
    gidtype = message.chat.type
    if gidtype in ["supergroup", "group"] and not await (GROUPS.find_one({"id": gid})):
        try:
            gidtitle = message.chat.username
        except KeyError:
            gidtitle = message.chat.title
        await GROUPS.insert_one({"id": gid, "grp": gidtitle})
        await clog("HELLBOT_MUSIC", f"Bot added to a new group\n\n{gidtitle}\nID: `{gid}`", "NEW_GROUP")
    if pycalls.pause(message.chat.id):
        await message.reply_text(f"**⏸ Paused !!**")
    else:
        await message.reply_text(f"**❗️ Nothing is playing to pause!**")


@hellbot.on_message(command(["resume", f"resume@{BUN}"]))
@errors
@authorized_users_only
async def resume(_, message: Message):
    gid = message.chat.id
    gidtype = message.chat.type
    if gidtype in ["supergroup", "group"] and not await (GROUPS.find_one({"id": gid})):
        try:
            gidtitle = message.chat.username
        except KeyError:
            gidtitle = message.chat.title
        await GROUPS.insert_one({"id": gid, "grp": gidtitle})
        await clog("HELLBOT_MUSIC", f"Bot added to a new group\n\n{gidtitle}\nID: `{gid}`", "NEW_GROUP")
    if pycalls.resume(message.chat.id):
        await message.reply_text(f"**🎧 Resumed !!**")
    else:
        await message.reply_text("**❗ Nothing is paused to resume!**")


@hellbot.on_message(command(["end", f"end@{BUN}"]))
@errors
@authorized_users_only
async def stop(_, message: Message):
    gid = message.chat.id
    gidtype = message.chat.type
    if gidtype in ["supergroup", "group"] and not await (GROUPS.find_one({"id": gid})):
        try:
            gidtitle = message.chat.username
        except KeyError:
            gidtitle = message.chat.title
        await GROUPS.insert_one({"id": gid, "grp": gidtitle})
        await clog("HELLBOT_MUSIC", f"Bot added to a new group\n\n{gidtitle}\nID: `{gid}`", "NEW_GROUP")
    if message.chat.id not in pycalls.active_chats:
        await message.reply_text("**❗ Not even playing!**")
    else:
        try:
            queue.clear(message.chat.id)
        except QueueEmpty:
            pass
        await pycalls.stop(message.chat.id)
        await message.reply_text("**✨ Cleared the queue cache and left the voice chat!!**")


@hellbot.on_message(command(["skip", "next", f"skip@{BUN}", f"next@{BUN}"]))
@errors
@authorized_users_only
async def skip(_, message: Message):
    gid = message.chat.id
    gidtype = message.chat.type
    if gidtype in ["supergroup", "group"] and not await (GROUPS.find_one({"id": gid})):
        try:
            gidtitle = message.chat.username
        except KeyError:
            gidtitle = message.chat.title
        await GROUPS.insert_one({"id": gid, "grp": gidtitle})
        await clog("HELLBOT_MUSIC", f"Bot added to a new group\n\n{gidtitle}\nID: `{gid}`", "NEW_GROUP")
    global que
    if gid not in pycalls.active_chats:
        await message.reply_text("**❗ Nothing is playing !!**")
    else:
        queue.task_done(gid)
        if queue.is_empty(gid):
            await pycalls.stop(gid)
        else:
            await pycalls.set_stream(gid, queue.get(gid)["file"])
    skipped = que.get(gid)
    if skipped:
        skipped.pop(0)
    if not skipped:
        return
    await message.reply_text(f"**⏭ Skipped !!**")


@hellbot.on_message(command(["mute", f"mute@{BUN}"]))
@errors
@authorized_users_only
async def mute(_, message: Message):
    gid = message.chat.id
    gidtype = message.chat.type
    if gidtype in ["supergroup", "group"] and not await (GROUPS.find_one({"id": gid})):
        try:
            gidtitle = message.chat.username
        except KeyError:
            gidtitle = message.chat.title
        await GROUPS.insert_one({"id": gid, "grp": gidtitle})
        await clog("HELLBOT_MUSIC", f"Bot added to a new group\n\n{gidtitle}\nID: `{gid}`", "NEW_GROUP")
    result = pycalls.mute(message.chat.id)
    if result == 0:
        await message.reply_text("🔇 **Muted !!**")
    elif result == 1:
        await message.reply_text("🔇 **Already muted !!**")
    elif result == 2:
        await message.reply_text("❗️**Voice chat isn't active!!**")


@hellbot.on_message(command(["unmute", f"unmute@{BUN}"]))
@errors
@authorized_users_only
async def unmute(_, message: Message):
    gid = message.chat.id
    gidtype = message.chat.type
    if gidtype in ["supergroup", "group"] and not await (GROUPS.find_one({"id": gid})):
        try:
            gidtitle = message.chat.username
        except KeyError:
            gidtitle = message.chat.title
        await GROUPS.insert_one({"id": gid, "grp": gidtitle})
        await clog("HELLBOT_MUSIC", f"Bot added to a new group\n\n{gidtitle}\nID: `{gid}`", "NEW_GROUP")
    result = pycalls.unmute(message.chat.id)
    if result == 0:
        await message.reply_text("🔊 **Unmuted !!**")
    elif result == 1:
        await message.reply_text("🔊 **Not even muted !!**")
    elif result == 2:
        await message.reply_text("❗️ **Voice chat isn't active !!**")


@hellbot.on_callback_query(filters.regex("cbpause"))
@admin_check
async def cbpause(_, query: CallbackQuery):
    if pycalls.pause(query.message.chat.id):
        await query.answer("⏸ Paused !!", show_alert=True)
    else:
        await query.answer("Nothing is playing", show_alert=True)

@hellbot.on_callback_query(filters.regex("cbresume"))
@admin_check
async def cbresume(_, query: CallbackQuery):
    if pycalls.resume(query.message.chat.id):
        await query.answer("🎧 Resumed !!", show_alert=True)
    else:
        await query.answer("Nothing is paused!", show_alert=True)

@hellbot.on_callback_query(filters.regex("cbend"))
@admin_check
async def cbend(_, query: CallbackQuery):
    if query.message.chat.id not in pycalls.active_chats:
        await query.answer("Nothing is playing!", show_alert=True)
    else:
        try:
            queue.clear(query.message.chat.id)
        except QueueEmpty:
            pass
        await pycalls.stop(query.message.chat.id)
        await query.answer("Cleared queue cache and left voice chat!", show_alert=True)

@hellbot.on_callback_query(filters.regex("cbskip"))
@admin_check
async def cbskip(_, query: CallbackQuery):
    if query.message.chat.id not in pycalls.active_chats:
        await query.answer("Nothing is playing!", show_alert=True)
    else:
        queue.task_done(query.message.chat.id)
        if queue.is_empty(query.message.chat.id):
            await pycalls.stop(query.message.chat.id)
        else:
            await pycalls.set_stream(query.message.chat.id, queue.get(query.message.chat.id)["file"])
        await query.answer("⏩ Skipped", show_alert=True)

@hellbot.on_callback_query(filters.regex("cbmute"))
@admin_check
async def cbmute(_, query: CallbackQuery):
    result = pycalls.mute(query.message.chat.id)
    if result == 0:
        await query.answer("🔇 Muted !!", show_alert=True)
    elif result == 1:
        await query.answer("🔇 Already Muted !!", show_alert=True)
    elif result == 2:
        await query.answer("Voice chat isn't active !!", show_alert=True)

@hellbot.on_callback_query(filters.regex("cbunmute"))
@admin_check
async def cbunmute(_, query: CallbackQuery):
    result = pycalls.unmute(query.message.chat.id)
    if result == 0:
        await query.answer("🔊 Unmuted !!", show_alert=True)
    elif result == 1:
        await query.answer("🔊 Not even muted !!", show_alert=True)
    elif result == 2:
        await query.answer("Voice chat isn't active !!", show_alert=True)

@hellbot.on_message(command(["auth", f"auth@{BUN}"]))
@authorized_users_only
async def authenticate(client: hellbot, message: Message):
    gid = message.chat.id
    gidtype = message.chat.type
    if gidtype in ["supergroup", "group"] and not await (GROUPS.find_one({"id": gid})):
        try:
            gidtitle = message.chat.username
        except KeyError:
            gidtitle = message.chat.title
        await GROUPS.insert_one({"id": gid, "grp": gidtitle})
        await clog("HELLBOT_MUSIC", f"Bot added to a new group\n\n{gidtitle}\nID: `{gid}`", "NEW_GROUP")
    global admins_dict
    if not message.reply_to_message:
        return await message.reply("**Reply to a user to authorise them.**")
    if message.reply_to_message.from_user.id not in admins_dict[message.chat.id]:
        new_admins = admins_dict[message.chat.id]
        new_admins.append(message.reply_to_message.from_user.id)
        admins_dict[message.chat.id] = new_admins
        await message.reply("**✨ User authorised to used admin commands.**")
    else:
        await message.reply("**✅ user already authorized!**")


@hellbot.on_message(command(["unauth", f"unauth@{BUN}"]))
@authorized_users_only
async def unautenticate(client: hellbot, message: Message):
    gid = message.chat.id
    gidtype = message.chat.type
    if gidtype in ["supergroup", "group"] and not await (GROUPS.find_one({"id": gid})):
        try:
            gidtitle = message.chat.username
        except KeyError:
            gidtitle = message.chat.title
        await GROUPS.insert_one({"id": gid, "grp": gidtitle})
        await clog("HELLBOT_MUSIC", f"Bot added to a new group\n\n{gidtitle}\nID: `{gid}`", "NEW_GROUP")
    global admins_dict
    if not message.reply_to_message:
        return await message.reply("Reply to a user to unauthorise them.")
    if message.reply_to_message.from_user.id in admins[message.chat.id]:
        new_admins = admins_dict[message.chat.id]
        new_admins.remove(message.reply_to_message.from_user.id)
        admins_dict[message.chat.id] = new_admins
        await message.reply("User removed from authorised list.")
    else:
        await message.reply("**Not even authorised!**")

@hellbot.on_message(filters.command(["delcmd", f"delcmd@{BUN}"]) & ~filters.private)
@authorized_users_only
async def delcmdc(_, message: Message):
    gid = message.chat.id
    gidtype = message.chat.type
    if gidtype in ["supergroup", "group"] and not await (GROUPS.find_one({"id": gid})):
        try:
            gidtitle = message.chat.username
        except KeyError:
            gidtitle = message.chat.title
        await GROUPS.insert_one({"id": gid, "grp": gidtitle})
        await clog("HELLBOT_MUSIC", f"Bot added to a new group\n\n{gidtitle}\nID: `{gid}`", "NEW_GROUP")
    if len(message.command) != 2:
        await message.reply_text("**Unknown command!!** \n\n__Give 'on' or 'off' along with /delcmd__")
        return
    status = message.text.split(" ", 1)[1]
    status = status.lower()
    chat_id = message.chat.id
    if status == "on":
        if await delcmd_is_on(message.chat.id):
            await message.reply_text("I'm already deleting commands spam in this chat.")
            return
        else:
            await delcmd_on(chat_id)
            await message.reply_text("I'll be deleting commands after execution.")
    elif status == "off":
        await delcmd_off(chat_id)
        await message.reply_text("I'll not delete commands in this chat now.")
    else:
        await message.reply_text("Give `/delcmd on` or `/delcmd off` only.")
