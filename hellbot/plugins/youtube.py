import time, os, math, asyncio, ffmpeg, requests, wget, yt_dlp

from urllib.parse import urlparse
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from youtubesearchpython import SearchVideos
from youtube_search import YoutubeSearch

from ..helper.database.db import get_collections
from ..helper.miscs import clog
from ..config import BOT_USERNAME as BUN
from ..helper.miscs import paste, capture_err

GROUPS = get_collections("GROUPS")
is_downloading = False

def humanbytes(size):
    if not size:
        return ""
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"

def time_formatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " day(s), ") if days else "")
        + ((str(hours) + " hour(s), ") if hours else "")
        + ((str(minutes) + " minute(s), ") if minutes else "")
        + ((str(seconds) + " second(s), ") if seconds else "")
        + ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    )
    return tmp[:-2]

async def progress(current, total, message, start, type_of_ps, file_name=None):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        if elapsed_time == 0:
            return
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "{0}{1} {2}%\n".format(
            "".join(["▓" for i in range(math.floor(percentage / 10))]),
            "".join(["░" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2),
        )
        tmp = progress_str + "{0} of {1}\nETA: {2}".format(
            humanbytes(current), humanbytes(total), time_formatter(estimated_total_time)
        )
        if file_name:
            try:
                await message.edit(
                    "{}\n**File Name:** `{}`\n{}".format(type_of_ps, file_name, tmp)
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass
        else:
            try:
                await message.edit("{}\n{}".format(type_of_ps, tmp))
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass


@Client.on_message(filters.command(['song', f'song@{BUN}']))
async def song(client, message):
    gid = message.chat.id
    gidtype = message.chat.type
    if gidtype in ["supergroup", "group"] and not await (GROUPS.find_one({"id": gid})):
        try:
            gidtitle = message.chat.username
        except KeyError:
            gidtitle = message.chat.title
        await GROUPS.insert_one({"id": gid, "grp": gidtitle})
        await clog("HELLBOT_MUSIC", f"Bot added to a new group\n\n{gidtitle}\nID: `{gid}`", "NEW_GROUP")
    user_ = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    qry = message.text
    query = qry.split(" ", 1)
    if len(query) == 1:
        return await message.reply("Give something to search and download 😑")
    m = await message.reply(f"<b><i>Searching for {query[1]} ...</i></b>")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query[1], max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)
        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]
    except Exception as e:
        await m.edit(
            f"<b><i>ERROR !!</b></i> \n\n<i>No song found. Maybe give different name or check spelling.</i> \n\n<code>{str(e)}</code>"
        )
        return
    await m.edit("<b><i>Got song... downloading now...</b></i>")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"<b><i>Title:</b></i> [{title[:35]}]({link}) \n<b><i>Duration:</b></i> <code>{duration}</code> \n<b><i>Views:</b></i> <code>{views}</code> \n\n<b><i>For:</b></i> {user_}"
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        await message.reply_audio(audio_file, caption=rep, thumb=thumb_name, performer="[ †hê Hêllẞø† ]" parse_mode='md', title=title, duration=dur)
        await m.delete()
    except Exception as e:
        await m.edit(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)


@Client.on_message(filters.command(["lyrics", f"lyrics@{BUN}"]))
async def lyrics_func(_, message):
    gid = message.chat.id
    gidtype = message.chat.type
    if gidtype in ["supergroup", "group"] and not await (GROUPS.find_one({"id": gid})):
        try:
            gidtitle = message.chat.username
        except KeyError:
            gidtitle = message.chat.title
        await GROUPS.insert_one({"id": gid, "grp": gidtitle})
        await clog("HELLBOT_MUSIC", f"Bot added to a new group\n\n{gidtitle}\nID: `{gid}`", "NEW_GROUP")
    qry = message.text
    query = qry.split(" ", 1)
    if len(query) == 1:
        await message.reply_text("<b><i>Mind giving what I should search ??</b></i>")
        return
    m = await message.reply_text(f"<b><i>Searching lyrics for {query[1]} ...</i></b>")
    song = await arq.lyrics(query[1])
    lyrics = song.result
    if len(lyrics) < 4095:
        await m.edit(f"__{lyrics}__")
        return
    lyrics = await paste(lyrics)
    await m.edit(f"<b><i>Lyrics was too long. Paste it <a href='{lurics}'>here</a>.</b></i>")


@Client.on_message(filters.command(["video", "vsong", f"video@{BUN}", f"vsong@{BUN}"]))
async def ytmusic(client, message: Message):
    gid = message.chat.id
    gidtype = message.chat.type
    if gidtype in ["supergroup", "group"] and not await (GROUPS.find_one({"id": gid})):
        try:
            gidtitle = message.chat.username
        except KeyError:
            gidtitle = message.chat.title
        await GROUPS.insert_one({"id": gid, "grp": gidtitle})
        await clog("HELLBOT_MUSIC", f"Bot added to a new group\n\n{gidtitle}\nID: `{gid}`", "NEW_GROUP")
    qry = message.text
    query = qry.split(" ", 1)
    global is_downloading
    if is_downloading:
        await message.reply_text("<b><i>I'm already downloading another video, try again later...</b></i>")
        return
    if len(query) == 1:
        return await message.reply_text("<b><i>Mind giving what I should search?</i></b>")
    pablo = await message.reply_text(f"<b><i>Searching {query[1]} ...</b></i>")
    search = SearchVideos(f"{query[1]}", offset=1, mode="dict", max_results=1)
    mi = search.result()
    mio = mi["search_result"]
    mo = mio[0]["link"]
    thum = mio[0]["title"]
    id_ = mio[0]["id"]
    thums = mio[0]["channel"]
    kekme = f"https://img.youtube.com/vi/{id_}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    url = mo
    sedlyf = wget.download(kekme)
    opts = {
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
        is_downloading = True
        with yt_dlp.YoutubeDL(opts) as ytdl:
            infoo = ytdl.extract_info(url, False)
            duration = round(infoo["duration"] / 60)

            if duration > 999:
                await pablo.edit(
                    f"<b><i>Searched video was {duration} minutes long and cancelled because maximum duration limit is 999 minutes.</b></i>"
                )
                is_downloading = False
                return
            ytdl_data = ytdl.extract_info(url, download=True)
    except Exception:
        is_downloading = False
        return
    c_time = time.time()
    file_ = f"{ytdl_data['id']}.mp4"
    YTVID_BUTTONS = InlineKeyboardMarkup([[InlineKeyboardButton("Watch on YT 📺", url=f"{mo}")]])
    capy = f"<b><i>Video Name:</b></i> <code>{thum}</code>"
    await client.send_video(
        message.chat.id,
        video=open(file_, "rb"),
        duration=int(ytdl_data["duration"]),
        file_name=str(ytdl_data["title"]),
        thumb=sedlyf,
        caption=capy,
        reply_markup=YTVID_BUTTONS,
        supports_streaming=True,
        progress=progress,
        progress_args=(
            pablo,
            c_time,
            f"<b><i>Wait, I'm downloading that...</b></i>",
            file_,
        ),
    )
    await pablo.delete()
    is_downloading = False
    for files in (sedlyf, file_):
        if files and os.path.exists(files):
            os.remove(files)
