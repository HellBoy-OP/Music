from HellMusic import bot, hell, client, trg
from pyrogram import filters
from pyrogram.types import Message


@bot.on_message(filters.command(["start", "alive"], prefixes=trg) & filters.private)
async def start(bot, message: Message):
    await message.reply_text("Alive!")
