from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant
from ..helper.decorators import errors, authorized_users_only
from .. import client as USER
from ..config import BOT_USERNAME as BUN


@Client.on_message(filters.group & filters.command(["join", f"join@{BUN}"]))
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b><i>Make sure I'm admin bruh 😥</b></i>",
        )
        return
    try:
        user = await USER.get_me()
    except:
        user.first_name =  "Hêllẞø† Music"
    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id,"<b><i>Okay!! Let's start music now?</b></i>")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b><i>Already here 👀</b></i>",
        )
        pass
    except Exception as e:
        print(e)
        await message.reply_text(f"<b><i>ERROR JOINING !!</b></i> \n\n<i>Maybe streaming account is banned here or we are facing flood wait issues due to heavy join requests. You can manually @{(await USER.get_me()).username} here.</i>")
        return
    await message.reply_text(
            "<b><i>Yeah! Why not...</b></i>")


@Client.on_message(filters.group & filters.command(["leave", f"leave@{BUN}"]))
@authorized_users_only
async def botleavegrp(client, message):
    await message.chat.leave()


@USER.on_message(filters.group & filters.command(["leave"]))
async def strmleavegrp(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text("<b><i>ERROR LEAVING !!!</i></b> \n\n<i>Unable to leave chat due to Floodwait Error. Remove me manually plox.</i>")
        return
