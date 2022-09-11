import os
import shutil
import yt_dlp
import asyncio
import requests
from config import Config
from pyrogram import filters
from HellMusic import bot, trg
from lyricsgenius import Genius
from HellMusic.plugins import BOT_UN
from pykeyboard import InlineKeyboard
from HellMusic.core.logging import LOGS
from HellMusic.core.client import client_id
from HellMusic.helpers.youtube import Hell_YTS
from HellMusic.helpers.error import parse_error
from HellMusic.helpers.paste import telegraph_paste
from HellMusic.helpers.text import CAPTION, PERFORMER
from HellMusic.helpers.tools import runcmd, absolute_paths
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from HellMusic.helpers.checks import check_mode


@bot.on_message(
    filters.command(["song", f"song@{BOT_UN}"], prefixes=trg) & ~filters.edited
)
async def songs(bot, message: Message):
    hell = await message.reply_text("Processing ...")
    mode = await check_mode(message)
    if mode == 0:
        return await hell.edit("You don't have access to use me.")
    lists = message.text.split(" ", 1)
    if len(lists) != 2:
        return await parse_error(hell, "Nothing given to search.")
    reply = message.reply_to_message
    hell_id, _, hell_mention = await client_id(message)
    query = lists[1].strip()
    if not query:
        return await parse_error(hell, "Nothing given to search.")
    await hell.edit(f"<b><i>Searching</i></b> “ `{query}` ”")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = Hell_YTS(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"thumb{hell_id}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        views = results[0]["views"]
        duration = results[0]["duration"]
    except Exception as e:
        return await parse_error(
            hell,
            f"__No song found. Maybe give different name or check spelling.__ \n`{str(e)}`",
            False,
        )
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        await hell.edit(
            f"**••• Uploading Song •••** \n\n__» {info_dict['title']}__\n__»» {info_dict['uploader']}__"
        )
        await message.reply_audio(
            audio=audio_file,
            caption=CAPTION.format(
                "Song", info_dict["title"], views, duration, hell_mention
            ),
            duration=int(info_dict["duration"]),
            performer=PERFORMER,
            title=info_dict["title"],
            thumb=thumb_name,
        )
        await hell.delete()
        try:
            os.remove(audio_file)
            os.remove(thumb_name)
        except BaseException:
            pass
    except Exception as e:
        await parse_error(hell, str(e))


@bot.on_message(
    filters.command(["video", f"video@{BOT_UN}"], prefixes=trg) & ~filters.edited
)
async def videos(bot, message: Message):
    hell = await message.reply_text("Processing ...")
    mode = await check_mode(message)
    if mode == 0:
        return await hell.edit("You don't have access to use me.")
    lists = message.text.split(" ", 1)
    if len(lists) != 2:
        return await parse_error(hell, "Nothing given to search.")
    reply = message.reply_to_message
    hell_id, _, hell_mention = await client_id(message)
    query = lists[1].strip()
    if not query:
        return await parse_error(hell, "Nothing given to search.")
    await hell.edit(f"<b><i>Searching</i></b> “ `{query}` ”")
    ydl_opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
    }
    try:
        results = Hell_YTS(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"thumb{hell_id}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        views = results[0]["views"]
        duration = results[0]["duration"]
    except Exception as e:
        return await parse_error(
            hell,
            f"__No song found. Maybe give different name or check spelling.__ \n`{str(e)}`",
            False,
        )
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            vid_file = ydl.extract_info(link, download=True)
        file_ = f"{vid_file['id']}.mp4"
        await hell.edit(
            f"**••• Uploading Video •••** \n\n__» {vid_file['title']}__\n__»» {vid_file['uploader']}__"
        )
        await message.reply_video(
            video=file_,
            caption=CAPTION.format(
                "Video", vid_file["title"], views, duration, hell_mention
            ),
            duration=int(vid_file["duration"]),
            supports_streaming=True,
        )
        await hell.delete()
        try:
            os.remove(file_)
            os.remove(thumb_name)
        except BaseException:
            pass
    except Exception as e:
        await parse_error(hell, e)


@bot.on_message(
    filters.command(["lyrics", f"lyrics@{BOT_UN}"], prefixes=trg) & ~filters.edited
)
async def lyrics(bot, message: Message):
    hell = await message.reply_text("Processing ...")
    mode = await check_mode(message)
    if mode == 0:
        return await hell.edit("You don't have access to use me.")
    if not Config.LYRICS_API:
        return await parse_error(hell, "`LYRICS_API` is not configured!", False)
    lists = message.text.split(" ", 1)
    if not len(lists) == 2:
        return await parse_error(
            hell,
            "__Nothing given to search.__ \nExample: `/lyrics loose yourself - eminem`",
            False,
        )
    _input_ = lists[1].strip()
    query = _input_.split("-", 1)
    if len(query) == 2:
        song = query[0].strip()
        artist = query[1].strip()
    else:
        song = query[0].strip()
        artist = ""
    text = f"**Searching lyrics ...** \n\n__Song:__ `{song}`"
    if artist != "":
        text += f"\n__Artist:__ `{artist}`"
    await hell.edit(text)
    LyClient = Genius(Config.LYRICS_API)
    results = LyClient.search_song(song, artist)
    if results:
        result = results.to_dict()
        title = result["full_title"]
        image = result["song_art_image_url"]
        lyrics = result["lyrics"]
        final = f"<b><i>• Song:</b></i> <code>{title}</code> \n<b><i>• Lyrics:</b></i> \n<code>{lyrics}</code>"
        if len(final) >= 4095:
            page_name = f"{title}"
            to_paste = f"<img src='{image}'/> \n{final} \n<img src='https://telegra.ph/file/2c546060b20dfd7c1ff2d.jpg'/>"
            link = await telegraph_paste(page_name, to_paste)
            await hell.edit(
                f"**Lyrics too big! Get it from here:** \n\n• [{title}]({link})",
                disable_web_page_preview=True,
            )
        else:
            await hell.edit(final)
    else:
        await parse_error(hell, "Unexpected Error Occured.")


@bot.on_message(
    filters.command(["spotify", f"spotify@{BOT_UN}"], prefixes=trg) & ~filters.edited
)
async def spotify(bot, message: Message):
    hell = await message.reply_text("Processing ...")
    mode = await check_mode(message)
    if mode == 0:
        return await hell.edit("You don't have access to use me.")
    hell_id, _, hell_mention = await client_id(message)
    reply = message.reply_to_message
    dirs = "./spotify/"
    lists = message.text.split(" ", 1)
    if not len(lists) == 2:
        return await parse_error(hell, "Nothing given to search on spotify.")
    query = lists[1].strip()
    await hell.edit(f"__Downloading__ `{query}` __from spotify ...__")
    cmd = (
        f"spotdl '{query}' --path-template 'spotify"
        + "/{artist}/{album}/{artist} - {title}.{ext}'"
    )
    await runcmd(cmd)
    art_list = os.listdir(dirs)
    dldirs = [i async for i in absolute_paths(dirs)]
    if len(dldirs) == 0:
        await hell.edit("Not found anything related to that.")
        await asyncio.sleep(10)
        await hell.delete()
        return
    for music in dldirs:
        try:
            await message.reply_audio(
                audio=music,
                caption=f"**✘ Spotify Song Downloaded !!** \n\n**« ✘ »** {hell_mention}",
                performer=PERFORMER,
            )
        except Exception as e:
            LOGS.error(str(e))
    try:
        shutil.rmtree("spotify")
        os.remove(".spotdl-cache")
    except BaseException:
        pass
    await hell.delete()
