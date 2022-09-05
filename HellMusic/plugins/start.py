from pyrogram import filters
from pyrogram.types import Message
from HellMusic import bot, trg, hell, client


@bot.on_message(filters.command(["start", "alive"], prefixes=trg) & filters.private)
async def start(bot, message: Message):
    await message.reply_text("Alive!")
