from os import path
from yt_dlp import YoutubeDL

from ..config import DURATION_LIMIT
from .errors import DurationLimitError

ytdl = YoutubeDL(
    {
        "format": "bestaudio/best",
        "geo-bypass": True,
        "nocheckcertificate": True,
        "outtmpl": "downloads/%(id)s.%(ext)s",
    }
)


def download(url: str) -> str:
    info = ytdl.extract_info(url, False)
    duration = round(info["duration"] / 60)

    if duration > DURATION_LIMIT:
        raise DurationLimitError(
            f"<b><i>!!! Requested video is {duration} minutes long which crosses my limit of {DURATION_LIMIT} minutes !!!</b></i>"
        )

    ytdl.download([url])
    return path.join("downloads", f"{info['id']}.{info['ext']}")
