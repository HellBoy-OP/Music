import asyncio
import traceback

from asyncio import QueueEmpty
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery

from ..helper import pycalls, queue
from ..helper.filters import command
from ..helper.decorators import errors, authorized_users_only
from ..helper.database.db import db, mdb_, Database
from ..helper.database.dbhelpers import handle_user_status, delcmd_is_on, delcmd_on, delcmd_off
from ..config import BOT_USERNAME as BUN
from . import que, admins as admins_dict


@Client.on_message()
async def _(bot: Client, cmd: Message):
    await handle_user_status(bot, cmd)


BACK_BUTTON = InlineKeyboardMarkup([[InlineKeyboardButton("Back ⬅️", callback_data="cbback")]])


async def delcmd(_, message: Message):
    if await delcmd_is_on(message.chat.id) and message.text.startswith("/") or message.text.startswith("!"):
        await message.delete()
    await message.continue_propagation()



@Client.on_message(filters.command(["reload", "admincache", f"reload@{BUN}", f"admincache@{BUN}"]))
@authorized_users_only
async def update_admin(client, message):
    global admins_dict
    admins = await client.get_chat_members(message.chat.id, filter="administrators")
    new_ads = []
    for u in admins:
        new_ads.append(u.user.id)
    admins_dict[message.chat.id] = new_ads
    await message.reply_text(f"**Admins List Refreshed !!**")
 
 
@Client.on_message(command(["control", f"control@{BUN}"]))
@errors
@authorized_users_only
async def controlset(_, message: Message):
    await message.reply_text(
        "**🕹️ Control Panel :**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Pause ⏸", callback_data="cbpause"
                    ),
                    InlineKeyboardButton(
                        "Resume ▶️", callback_data="cbresume"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Skip ⏩", callback_data="cbskip"
                    ),
                    InlineKeyboardButton(
                        "End ⏹", callback_data="cbend"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Mute 🔇", callback_data="cbmute"
                    ),
                    InlineKeyboardButton(
                        "Unmute 🔊", callback_data="cbunmute"
                    )
                ]
            ]
        )
    )



@Client.on_message(command(["pause", f"pause@{BUN}"]))
@errors
@authorized_users_only
async def pause(_, message: Message):
    if pycalls.pause(message.chat.id):
        await message.reply_text(f"**⏸ Paused !!**")
    else:
        await message.reply_text(f"**❗️ Nothing is playing to pause!**")


@Client.on_message(command(["resume", f"resume@{BUN}"]))
@errors
@authorized_users_only
async def resume(_, message: Message):
    if pycalls.resume(message.chat.id):
        await message.reply_text(f"**🎧 Resumed !!**")
    else:
        await message.reply_text("**❗ Nothing is paused to resume!**")


@Client.on_message(command(["end", f"end@{BUN}"]))
@errors
@authorized_users_only
async def stop(_, message: Message):
    if message.chat.id not in pycalls.active_chats:
        await message.reply_text("**❗ Not even playing!**")
    else:
        try:
            queue.clear(message.chat.id)
        except QueueEmpty:
            pass
        await pycalls.stop(message.chat.id)
        await message.reply_text("**✨ Cleared the queue cache and left the voice chat!!**")


@Client.on_message(command(["skip", "next", f"skip@{BUN}", f"next@{BUN}"]))
@errors
@authorized_users_only
async def skip(_, message: Message):
    if message.chat.id not in pycalls.active_chats:
        await message.reply_text("**❗ Nothing is playing !!**")
    else:
        queue.task_done(message.chat.id)
        if queue.is_empty(message.chat.id):
            await pycalls.stop(message.chat.id)
        else:
            await pycalls.set_stream(
                message.chat.id, queue.get(message.chat.id)["file"]
            )
        await message.reply_text(f"⏭ Skipped !!**")


@Client.on_message(command(["mute", f"mute@{BUN}"]))
@errors
@authorized_users_only
async def mute(_, message: Message):
    result = pycalls.mute(message.chat.id)
    if result == 0:
        await message.reply_text("🔇 **Muted !!**")
    elif result == 1:
        await message.reply_text("🔇 **Already muted !!**")
    elif result == 2:
        await message.reply_text("❗️**Voice chat isn't active!!**")


@Client.on_message(command(["unmute", f"unmute@{BUN}"]))
@errors
@authorized_users_only
async def unmute(_, message: Message):
    result = pycalls.unmute(message.chat.id)
    if result == 0:
        await message.reply_text("🔊 **Unmuted !!**")
    elif result == 1:
        await message.reply_text("🔊 **Not even muted !!**")
    elif result == 2:
        await message.reply_text("❗️ **Voice chat isn't active !!**")


@Client.on_callback_query(filters.regex("cbpause"))
async def cbpause(_, query: CallbackQuery):
    if pycalls.pause(query.message.chat.id):
        await query.edit_message_text("⏸ Paused !!**", reply_markup=BACK_BUTTON)
    else:
        await query.edit_message_text("❗️ **Nothing is playing to pause!**", reply_markup=BACK_BUTTON)

@Client.on_callback_query(filters.regex("cbresume"))
async def cbresume(_, query: CallbackQuery):
    if pycalls.resume(query.message.chat.id):
        await query.edit_message_text("🎧 **Resumed !!**", reply_markup=BACK_BUTTON)
    else:
        await query.edit_message_text("❗️ **Nothing is paused to resume!**", reply_markup=BACK_BUTTON)

@Client.on_callback_query(filters.regex("cbend"))
async def cbend(_, query: CallbackQuery):
    if query.message.chat.id not in pycalls.active_chats:
        await query.edit_message_text("❗️**Nothing is playing to end!**", reply_markup=BACK_BUTTON)
    else:
        try:
            queue.clear(query.message.chat.id)
        except QueueEmpty:
            pass

        await pycalls.stop(query.message.chat.id)
        await query.edit_message_text("✅ **Cleared queue cache and left voice chat!**", reply_markup=BACK_BUTTON)

@Client.on_callback_query(filters.regex("cbskip"))
async def cbskip(_, query: CallbackQuery):
     if query.message.chat.id not in pycalls.active_chats:
        await query.edit_message_text("❗️ **Nothing is playing to skip!**", reply_markup=BACK_BUTTON)
     else:
        queue.task_done(query.message.chat.id)
        if queue.is_empty(query.message.chat.id):
            await pycalls.stop(query.message.chat.id)
        else:
            await pycalls.set_stream(
                query.message.chat.id, queue.get(query.message.chat.id)["file"]
            )

        await query.edit_message_text("⏩ **Skipped**", reply_markup=BACK_BUTTON)

@Client.on_callback_query(filters.regex("cbmute"))
async def cbmute(_, query: CallbackQuery):
    result = pycalls.mute(query.message.chat.id)

    if result == 0:
        await query.edit_message_text("🔇 **Muted !!**", reply_markup=BACK_BUTTON)
    elif result == 1:
        await query.edit_message_text("🔇 **Already Muted !!**", reply_markup=BACK_BUTTON)
    elif result == 2:
        await query.edit_message_text("❗️ **Voice chat isn't active !!**", reply_markup=BACK_BUTTON)

@Client.on_callback_query(filters.regex("cbunmute"))
async def cbunmute(_, query: CallbackQuery):
    result = pycalls.unmute(query.message.chat.id)

    if result == 0:
        await query.edit_message_text("🔊 **Unmuted !!**", reply_markup=BACK_BUTTON)
    elif result == 1:
        await query.edit_message_text("🔊  **Not even muted !!**", reply_markup=BACK_BUTTON)
    elif result == 2:
        await query.edit_message_text("❗️ **Voice chat isn't active !!**", reply_markup=BACK_BUTTON)

@Client.on_message(command(["auth", f"auth@{BUN}"]))
@authorized_users_only
async def authenticate(client, message):
    global admins
    if not message.reply_to_message:
        return await message.reply("**Reply to a user to authorise them.**")
    if message.reply_to_message.from_user.id not in admins[message.chat.id]:
        new_admins = admins[message.chat.id]
        new_admins.append(message.reply_to_message.from_user.id)
        admins[message.chat.id] = new_admins
        await message.reply(
            "**✨ User authorised to used admin commands.**"
        )
    else:
        await message.reply("**✅ user already authorized!**")


@Client.on_message(command(["unauth", f"unauth@{BUN}"]))
@authorized_users_only
async def unautenticate(client, message):
    global admins
    if not message.reply_to_message:
        return await message.reply("Reply to a user to unauthorise them.")
    if message.reply_to_message.from_user.id in admins[message.chat.id]:
        new_admins = admins[message.chat.id]
        new_admins.remove(message.reply_to_message.from_user.id)
        admins[message.chat.id] = new_admins
        await message.reply(
            "User removed from authorised list."
        )
    else:
        await message.reply("**Not even authorised!**")

@Client.on_message(filters.command(["delcmd", f"delcmd@{BUN}"]) & ~filters.private)
@authorized_users_only
async def delcmdc(_, message: Message):
    if len(message.command) != 2:
        await message.reply_text("**Unknown command!!** \n\n__Give 'on' or 'off' along with /delcmd__")
        return
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    if status == "on":
        if await delcmd_is_on(message.chat.id):
            await message.reply_text("I'm already deleting commands spam in this chat.")
            return
        else:
            await delcmd_on(chat_id)
            await message.reply_text(
                "I'll be deleting commands after execution."
            )
    elif status == "off":
        await delcmd_off(chat_id)
        await message.reply_text("I'll not delete commands in this chat now.")
    else:
        await message.reply_text(
            "Give `/delcmd on` or `/delcmd off` only."
        )
