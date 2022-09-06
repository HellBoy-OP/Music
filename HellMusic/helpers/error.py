import asyncio


async def parse_error(message, error, auto_parse=True, delete=True, time=10):
    if delete:
        if auto_parse:
            hell = await message.edit(f"**ERROR !!** \n\n`{error}`")
            await asyncio.sleep(time)
            await hell.delete()
        else:
            hell = await message.edit(f"**ERROR !!** \n\n{error}")
            await asyncio.sleep(time)
            await hell.delete()
    else:
        if auto_parse:
            await message.edit(f"**ERROR !!** \n\n`{error}`")
        else:
            await message.edit(f"**ERROR !!** \n\n{error}")
