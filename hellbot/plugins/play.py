from os import path
from pyrogram import Client, filters
from pyrogram.types import Message, Voice, InlineKeyboardMarkup, InlineKeyboardButton
from youtube_search import YoutubeSearch

from ..config import DURATION_LIMIT, BOT_USERNAME as BUN, THUMB_URL
from ..helper import pycalls, queue, converter, youtube
from ..helper.database.db import get_collections
from ..helper.database.dbhelpers import handle_user_status
from ..helper.decorators import errors
from ..helper.errors import DurationLimitError
from ..helper.filters import command, grp_filters
from ..helper.miscs import clog

GROUPS = get_collections("GROUPS")

@Client.on_message(filters.private)
async def _(bot: Client, cmd: command):
    await handle_user_status(bot, cmd)


@Client.on_message(command(["play", f"play@{BUN}"]) & grp_filters)
@errors
async def play(_, message: Message):
    gid = message.chat.id
    gidtype = message.chat.type
    if gidtype in ["supergroup", "group"] and not await (GROUPS.find_one({"id": gid})):
        try:
            gidtitle = message.chat.username
        except KeyError:
            gidtitle = message.chat.title
        await GROUPS.insert_one({"id": gid, "grp": gidtitle})
        await clog("HELLBOT_MUSIC", f"Bot added to a new group\n\n{gidtitle}\nID: `{gid}`", "NEW_GROUP")
    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    user_ = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    qry = message.text.split(" ", 1)
    is_yt = False
    response = await message.reply_text("<b><i>Processing ...</b></i>")
    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"<b><i>Actually there's a duration limit and this audio crossed that. My limit is {DURATION_LIMIT} minutes.</b></i>"
            )
        await response.edit("<b><i>Audio File Detected!! Processing...</b></i>")
        file_name = audio.file_unique_id + "." + (
            (
                audio.file_name.split(".")[-1]
            ) if (
                not isinstance(audio, Voice)
            ) else "ogg"
        )
        file = await converter.convert(
            (
                await message.reply_to_message.download(file_name)
            )
            if (
                not path.isfile(path.join("downloads", file_name))
            ) else file_name
        )
    elif len(qry) > 1:
        if qry[1].startswith("https://youtu"):
            await response.edit("<b><i>Youtube Url Detected!! Processing...</b></i>")
            url = qry[1]
            file = await converter.convert(youtube.download(url))
        else:
            await response.edit(f"<b><i>Searching “ {qry[1]} ” on Youtube...</i></b>")
            try:
                results = YoutubeSearch(qry[1], max_results=1).to_dict()
                duration = results[0]["duration"]
                title = results[0]["title"][:40]
                url = f"https://youtube.com{results[0]['url_suffix']}"
            except Exception as e:
                await response.edit(f"<b><i>ERROR !!</i></b> \n\n<code>{str(e)}</code>")
                return
            try:
                sec, dur, dur_arr = 1, 0, duration.split(':')
                for i in range(len(dur_arr)-1, -1, -1):
                    dur += (int(dur_arr[i]) * sec)
                    sec *= 60
                if (dur / 60) > DURATION_LIMIT:
                    await response.edit(f"<b><i>Requested Song was longer than {DURATION_LIMIT} minutes. ABORTING PROCESS!!</i></b>")
                    return
            except:
                pass
            file = await converter.convert(youtube.download(url))
            is_yt = True
    else:
        await response.edit("<b><i>Give something to play.</i></b>")
        return
    if message.chat.id in pycalls.active_chats:
        position = await queue.put(message.chat.id, file)
        await response.delete()
        if is_yt:
            await message.reply_photo(
                THUMB_URL,
                f"<b><i>• Song Name:</b>/i> <a href='{url}'>{title[:20]}...</a> \n<b><i>• Duration:</b></i> <code>{duration}</code> \n<b><i>• Requested By:</i></b> {user_} \n<b><i>• Status:</b></i> <code>#{position} in queue</code>",
                reply_markup=btns,
            )
        else:
            await message.reply_text(
                THUMB_URL,
                f"<b><i>Playing Selected File !!</b></i> \n<b><i>Requested By:</b></i> {user_} \n<b><i>• Status:</b></i> <code>#{position} in queue</code>",
                reply_markup=btns,
            )
    else:
        await pycalls.set_stream(message.chat.id, file)
        await response.delete()
        if is_yt:
            await message.reply_photo(
                THUMB_URL,
                f"<b><i>• Song Name:</b>/i> <a href='{url}'>{title[:20]}...</a> \n<b><i>• Duration:</b></i> <code>{duration}</code> \n<b><i>• Requested By:</i></b> {user_} \n<b><i>• Status:</b></i> <code>Started Playing</code>",
                reply_markup=btns,
            )
        else:
            await message.reply_text(
                THUMB_URL,
                f"<b><i>Playing Selected File !!</b></i> \n<b><i>Requested By:</b></i> {user_} \n<b><i>• Status:</b></i> <code>Started Playing</code>",
                reply_markup=btns,
            )
