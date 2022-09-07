from pyrogram import filters
from pyrogram.types import Message
from HellMusic import bot, trg, hell, client
from HellMusic.helpers.text import START_GC, START_PM


@bot.on_message(
    filters.command(["start", "alive"], prefixes=trg) & filters.private
)
async def start_pm(bot, message: Message):
    await message.reply_text(START_PM)


@bot.on_message(
    filters.command(["start", "alive"], prefixes=trg) & ~filters.private
)
async def start_gc(bot, message: Message):
    await message.reply_text(START_GC)
