import glob
import logging
from pathlib import Path

from . import hellbot, client, run, load_plugins, group_call_instances


@client.on_message(filters.me & filters.command("start"))
async def pl(__, _):
    if _.chat.id in group_call_instances.active_chats:
        queues.put(_.chat.id, 'out.raw')
    else:
        await group_call_instances.set_stream(_.chat.id, 'out.raw')


@client.on_message(filters.me & filters.command("end"))
async def pl(__, _):
    await group_call_instances.stop(_.chat.id)


hellbot.start()
client.run()
run()

print("!!! HellBot Music Start-up Complete !!!")

