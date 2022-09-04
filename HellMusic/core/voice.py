import sys
from config import Config
from pyrogram import Client
from HellMusic.core.logging import LOGS
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.exceptions import NoActiveGroupCall, AlreadyJoinedError


class HellVoice(PyTgCalls):
    def __init__(self):
        self.user = Client(
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            session_name=str(Config.HELLBOT_SESSION),
        )
        self.tgcalls = PyTgCalls(self.user, 100)

    async def start(self):
        LOGS.info("••• Starting Hell-Music Voice •••")
        if Config.HELLBOT_SESSION:
            await self.tgcalls.start()
        else:
            LOGS.info("[HELLBOT_SESSION]: Invalid string session!")
            sys.exit()

    async def ping(self):
        pinged = await self.tgcalls.ping
        return pinged

    async def join_vc(
        self,
        chat_id: int,
        link: str,
        video: bool,
        quality: list,
    ):
        stream = None
        audio_quality, video_quality = quality
        if video:
            stream = AudioVideoPiped(
                link,
                audio_quality,
                video_quality,
            )
        else:
            stream = AudioPiped(
                link,
                audio_quality,
            )
        if stream:
            try:
                await self.tgcalls.join_group_call(
                    chat_id,
                    stream,
                    stream_type=StreamType().pulse_stream,
                )
                return "joined"
            except NoActiveGroupCall:
                error = "No Active Voice Chat Found!"
                LOGS.error(error)
                return error
            except AlreadyJoinedError:
                error = "Music client is already in the voice chat!"
                LOGS.error(error)
                return error
            except Exception as e:
                LOGS.error(str(e))
                return str(e)
        else:
            error = "There was a problem in stream processing! Try again later."
            LOGS.error(error)
            return error

    async def cache(self):
        cached = await self.tgcalls.cache_peer
        return cached

    async def pause(self, chat_id: int):
        await self.tgcalls.pause_stream(chat_id)
        return "paused"

    async def resume(self, chat_id: int):
        await self.tgcalls.resume_stream(chat_id)
        return "resumed"

    async def stop(self, chat_id: int):
        await self.tgcalls.leave_group_call(chat_id)
        return "left"

    async def mute(self, chat_id: int):
        await self.tgcalls.mute_stream(chat_id)
        return "muted"

    async def unmute(self, chat_id: int):
        await self.tgcalls.unmute_stream(chat_id)
        return "unmuted"

    async def volume(self, chat_id: int, volume: int):
        await self.tgcalls.change_volume_call(chat_id, volume)
        return "changed"

    async def active_calls(self):
        active = await self.tgcalls.active_calls
        return active

    async def calls(self):
        call = await self.tgcalls.calls
        return call

    async def get_active_call(self, chat_id: int):
        active_call = await self.tgcalls.get_active_call(chat_id)
        return active_call

    async def get_call(self, chat_id: int):
        call = await self.tgcalls.get_calls(chat_id)
        return call

    async def participants(self, chat_id: int):
        members = await self.tgcalls.get_participants(chat_id)
        return members

    async def seek_vc(
        self,
        chat_id: int,
        link: str,
        video: bool,
        quality: list,
        duration: int,
        seek: int,
    ):
        stream = None
        audio_quality, video_quality = quality
        cmd = f"-ss {seek} -to {duration}"
        if video:
            stream = AudioVideoPiped(
                link,
                audio_quality,
                video_quality,
                additional_ffmpeg_parameters=cmd,
            )
        else:
            stream = AudioPiped(
                link,
                audio_quality,
                additional_ffmpeg_parameters=cmd,
            )
        if stream:
            try:
                await self.tgcalls.change_stream(chat_id, stream)
            except Exception as e:
                LOGS.error(str(e))
                return str(e)

    async def new_stream(
        self,
        chat_id: int,
        link: str,
        video: bool,
        quality: list,
    ):
        stream = None
        audio_quality, video_quality = quality
        if video:
            stream = AudioVideoPiped(
                link,
                audio_quality,
                video_quality,
            )
        else:
            stream = AudioPiped(
                link,
                audio_quality,
            )
        if stream:
            try:
                await self.tgcalls.change_stream(chat_id, stream)
            except Exception as e:
                LOGS.error(str(e))
                return str(e)
