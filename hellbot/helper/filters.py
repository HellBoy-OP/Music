from typing import Union, List
from pyrogram import filters

from ..config import HANDLER


grp_filters = filters.group & ~ filters.edited & ~ filters.via_bot & ~ filters.forwarded
pvt_filters = filters.private & ~ filters.edited & ~ filters.via_bot & ~ filters.forwarded


def command(commands: Union[str, List[str]]):
    return filters.command(commands, HANDLER)
