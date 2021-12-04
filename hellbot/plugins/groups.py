from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant

from ..helper.database.db import get_collections
from ..helper.decorators import errors, authorized_users_only
from ..helper.miscs import clog
from .. import client as USER, hellbot
from ..config import BOT_USERNAME as BUN

GROUPS = get_collections("GROUPS")

@hellbot.on_message(filters.group & filters.command(["join", f"join@{BUN}"]))
@authorized_users_only
@errors
async def addchannel(client: hellbot, message: Message):
    gid = message.chat.id
    gidtype = message.chat.type
    if gidtype in ["supergroup", "group"] and not await (GROUPS.find_one({"id": gid})):
        try:
            gidtitle = message.chat.username
        except KeyError:
            gidtitle = message.chat.title
        await GROUPS.insert_one({"id": gid, "grp": gidtitle})
        await clog("HELLBOT_MUSIC", f"Bot added to a new group\n\n{gidtitle}\nID: `{gid}`", "NEW_GROUP")
    try:
        invitelink = await client.export_chat_invite_link(gid)
    except:
        await message.reply_text("<b><i>Make sure I'm admin with invite users permission...😥</b></i>")
        return
    try:
        user = await USER.get_me()
    except:
        user.first_name =  "Hêllẞø† Music"
    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id,"<b><i>Okay!! Let's start music now?</b></i>")
    except UserAlreadyParticipant:
        await message.reply_text("<b><i>Already here 👀</b></i>")
        pass
    except Exception as e:
        print(str(e))
        await message.reply_text(f"<b><i>ERROR JOINING !!</b></i> \n\n<i>Maybe streaming account is banned here or we are facing flood wait issues due to heavy join requests. You can manually @{(await USER.get_me()).username} here.</i>")
        return
    await message.reply_text("<b><i>Yeah! Why not...</b></i>")


@hellbot.on_message(filters.group & filters.command(["leave", f"leave@{BUN}"]))
@authorized_users_only
async def botleavegrp(client: hellbot, message: Message):
    gid = message.chat.id
    gidtype = message.chat.type
    if gidtype in ["supergroup", "group"] and not await (GROUPS.find_one({"id": gid})):
        try:
            gidtitle = message.chat.username
        except KeyError:
            gidtitle = message.chat.title
        await GROUPS.insert_one({"id": gid, "grp": gidtitle})
        await clog("HELLBOT_MUSIC", f"Bot added to a new group\n\n{gidtitle}\nID: `{gid}`", "NEW_GROUP")
    await message.chat.leave()


@USER.on_message(filters.group & filters.command(["leave"]))
async def strmleavegrp(client: USER, message: Message):
    try:
        await client.leave_chat(message.chat.id)
    except:
        await message.reply_text("<b><i>ERROR LEAVING !!!</i></b> \n\n<i>Unable to leave chat due to Floodwait Error. Remove me manually plox.</i>")
        return
