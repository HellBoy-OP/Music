import os
import json
import wget
from . import que
from os import path
from ..helper.miscs import clog
from .. import arq, client, hellbot
from pyrogram import Client, filters
from ..helper.decorators import errors
from youtube_search import YoutubeSearch
from ..helper.errors import DurationLimitError
from ..helper.database.db import get_collections
from ..helper.filters import command, grp_filters
from ..helper import queue, pycalls, youtube, converter
from ..config import BOT_USERNAME as BUN, DURATION_LIMIT
from ..helper.database.dbhelpers import handle_user_status
from pyrogram.types import (
    Voice, Message, InlineKeyboardButton, InlineKeyboardMarkup)


GROUPS = get_collections("GROUPS")


@hellbot.on_message(filters.private)
async def _(bot: hellbot, cmd: command):
    await handle_user_status(bot, cmd)


btns = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Pause ⏸", callback_data="cbpause"),
            InlineKeyboardButton("Resume ▶️", callback_data="cbresume"),
        ],
        [
            InlineKeyboardButton("Skip ⏩", callback_data="cbskip"),
            InlineKeyboardButton("End ⏹", callback_data="cbend"),
        ],
        [InlineKeyboardButton("Close 🗑️", callback_data="close")],
    ]
)


@hellbot.on_message(command(["play", f"play@{BUN}"]) & grp_filters)
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
        await clog(
            "HELLBOT_MUSIC",
            f"Bot added to a new group\n\n{gidtitle}\nID: `{gid}`",
            "NEW_GROUP",
        )
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    user_ = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    qry = message.text.split(" ", 1)
    if not message.reply_to_message and len(qry) == 1:
        return await message.reply_text("<b><i>Give something to play!!</b></i>")
    is_yt = False
    response = await message.reply_text("<b><i>Processing ...</b></i>")
    if audio:
        if round(audio.duration / 60) > int(DURATION_LIMIT):
            raise DurationLimitError(
                f"<b><i>Actually there's a duration limit and this audio crossed that. My limit is {DURATION_LIMIT} minutes.</b></i>"
            )
        await response.edit("<b><i>Audio File Detected!! Processing...</b></i>")
        file_name = (
            audio.file_unique_id
            + "."
            + (
                (audio.file_name.split(".")[-1])
                if (not isinstance(audio, Voice))
                else "ogg"
            )
        )
        file = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if (not path.isfile(path.join("downloads", file_name)))
            else file_name
        )
        title = "Selected Audio File"
        views = "Unknown"
        duration = audio.duration
    elif "-s" in qry[1][-2:]:
        try:
            await response.edit(
                f"<b><i>Searching “ {qry[1][:-2].strip()} ” on Saavn...</i></b>",
                disable_web_page_preview=True,
            )
            song = await arq.saavn(qry[1][:-2].strip())
            if not song.ok:
                return await message.reply_text(song.result)
            title = song.result[0].song
            url = song.result[0].media_url
            duration = int(song.result[0].duration)
            views = "Unknown"
        except Exception as e:
            await response.edit("<b><i>Unable to find that song.</b></i>")
            print(str(e))
            return
        file = await converter.convert(wget.download(url))
        is_yt = True
    else:
        await response.edit(
            f"<b><i>Searching “ {qry[1]} ” on Youtube...</i></b>",
            disable_web_page_preview=True,
        )
        try:
            results = json.loads(YoutubeSearch(qry[1], max_results=1).to_json())
        except KeyError:
            return await response.edit(
                "<b><i>ERROR !!</b></i> \n\n<i>Unable to find relevant search queries...</i>"
            )
        for i in results["videos"]:
            url = f"https://www.youtube.com{i['url_suffix']}"
            duration = i["duration"]
            title = i["title"][:50]
            views = i["views"]
        file = await converter.convert(youtube.download(url))
        is_yt = True
    await converter.thumbnail_convert(title, views, duration)
    if gid in pycalls.active_chats:
        position = await queue.put(gid, file=file)
        queue_ = que.get(gid)
        usr_id = message.from_user.id
        things_ = [title, usr_id, file]
        queue_.append(things_)
        await response.delete()
        if is_yt:
            await message.reply_photo(
                photo="final.png",
                caption=f"<b><i>• Song Name:</b></i> <a href='{url}'>{title}...</a> \n<b><i>• Duration:</b></i> <code>{duration}</code> \n<b><i>• Views:</b></i> <code>{views}</code> \n<b><i>• Requested By:</i></b> {user_} \n<b><i>• Status:</b></i> <code>#{position} in queue</code>",
                reply_markup=btns,
            )
        else:
            await message.reply_photo(
                photo="final.png",
                caption=f"<b><i>Playing Selected File !!</b></i> \n<b><i>Requested By:</b></i> {user_} \n<b><i>• Status:</b></i> <code>#{position} in queue</code>",
                reply_markup=btns,
            )
    else:
        que[gid] = []
        queue_ = que.get(gid)
        usr_id = message.from_user.id
        things_ = [title, usr_id, file]
        queue_.append(things_)
        await pycalls.set_stream(gid, file=file)
        await response.delete()
        if is_yt:
            await message.reply_photo(
                photo="final.png",
                caption=f"<b><i>• Song Name:</b></i> <a href='{url}'>{title}...</a> \n<b><i>• Duration:</b></i> <code>{duration}</code> \n<b><i>• Views:</b></i> <code>{views}</code> \n<b><i>• Requested By:</i></b> {user_} \n<b><i>• Status:</b></i> <code>Started Playing</code>",
                reply_markup=btns,
            )
        else:
            await message.reply_photo(
                photo="final.png",
                caption=f"<b><i>Playing Selected File !!</b></i> \n<b><i>Requested By:</b></i> {user_} \n<b><i>• Status:</b></i> <code>Started Playing</code>",
                reply_markup=btns,
            )
    os.remove("final.png")
