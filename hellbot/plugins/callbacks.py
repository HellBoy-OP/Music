from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery

from ..helper.database.db import get_collections
from ..helper.miscs import clog
from .. import client as USER
from ..config import BOT_USERNAME as BUN, OWNER

BOT_PIC = "https://te.legra.ph/file/2a24a198476d4abf505da.jpg"


@Client.on_callback_query(filters.regex("close"))
async def close(_, query: CallbackQuery):
    await query.message.delete()


@Client.on_callback_query(filters.regex("cbback"))
async def cbback(_, query: CallbackQuery):
    await query.edit_message_text(
        text="**Hêllẞø† Control Panel :**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Pause ⏸", callback_data="cbpause"
                    ),
                    InlineKeyboardButton(
                        "Resume ▶️", callback_data="cbresume"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Skip ⏩", callback_data="cbskip"
                    ),
                    InlineKeyboardButton(
                        "End ⏹", callback_data="cbend"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Mute 🔇", callback_data="cbmute"
                    ),
                    InlineKeyboardButton(
                        "Unmute 🔊", callback_data="cbunmute"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.edit_message_caption(
        caption=f"<b><i>Hello there!! \nI'm a Telegram voice chat music player by @Its_Hellbot. Enjoy my advanced features along with a simple and sexy interface</b></i>",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Add in group 🦜", url=f"https://t.me/{BUN}?startgroup=true")
                ],
                [
                    InlineKeyboardButton("Guide 📜", callback_data="cbhowtouse"),
                    InlineKeyboardButton("Commands 📌", callback_data="cbcmds")
                ],
                [
                    InlineKeyboardButton("Channel 🍀", url="https://t.me/its_hellbot"),
                    InlineKeyboardButton("Source Code", url="https://github.com/The-HellBot/Music")
                ],
                [
                    InlineKeyboardButton("Deployed By", url=f"tg://openmessage?user_id={OWNER}")
                ],
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbhelpmenu"))
async def cbhelpmenu(_, query: CallbackQuery):
    await query.edit_message_text(
        caption=f"""<b><i>Hello there {query.message.from_user.mention} 😉️!</b></i>
<i>Here is the help menu and some basic guide:</i>""",
        reply_markup=InlineKeyboardMarkup([InlineKeyboardButton("How to use ❓", callback_data="cbhowtouse")])
    )


@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbhowtouse(client: Client, query: CallbackQuery):
    await client.send_message(
        query.message.chat.id,
        text=f"<b><i>How to use me?</b></i>\n\n<b>Step 1:</b> <i>Add me( @{BUN} ) and @{(await USER.get_me()).username} in your group or just add me and send /join for automatic joining process.</i>\n<b>Step 2:</b> <i>Promote me ( @{BUN} ) and @{(await USER.get_me()).username} with atleast Manage Voice Chat rights.</i>\n\n<i>Done! You are good to go. Now see my command menu to get details of commands I support.</i>\n\n<b><i>By:</b></i> @Its_HellBot",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Commands 📌", callback_data="cbcmds")
                ],
                [
                    InlineKeyboardButton("Close 🗑️", callback_data="close")
                ],
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbcmds"))
async def cbcmds(client: Client, query: CallbackQuery):
    await client.send_message(
        query.message.chat.id,
        text=f"<b><i>📝 Below are my list of commands I currently support:</b></i>",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Admin & Sudo", callback_data="cbadmins"),
                    InlineKeyboardButton("Owner", callback_data="cbowner")
                ],
                [
                    InlineKeyboardButton("Downloads", callback_data="cbdwl"),
                    InlineKeyboardButton("Extras", callback_data="cbextras")
                ],
                [
                    InlineKeyboardButton("Voice Chat", callback_data="cbvc"),
                    InlineKeyboardButton("Others", callback_data="cbothers")
                ],
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbcmd"))
async def cbcmds(client: Client, query: CallbackQuery):
    await query.edit_message_text(
        text=f"<b><i>📝 Below are my list of commands I currently support:</b></i>",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Admin & Sudo", callback_data="cbadmins"),
                    InlineKeyboardButton("Owner", callback_data="cbowner")
                ],
                [
                    InlineKeyboardButton("Downloads", callback_data="cbdwl"),
                    InlineKeyboardButton("Extras", callback_data="cbextras")
                ],
                [
                    InlineKeyboardButton("Voice Chat", callback_data="cbvc"),
                    InlineKeyboardButton("Others", callback_data="cbothers")
                ],
                [
                    InlineKeyboardButton("Close", callback_data="close")
                ],
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbothers"))
async def cbothers(_, query: CallbackQuery):
    await query.edit_message_text(
        text=f"""
<b><i>Some Other Commands:</b></i>

<b>1. Command:</b> <code>/lyrics song name</code>
<b>    Usage:</b> <code>Gets you the lyrics of given song.</code>
<b>    Example:</b> <code>/lyrics perfect</code>

<b>2. Command:</b> <code>/search query</code>
<b>    Usage:</b> <code>Searches youtube video links.</code>
<b>    Example:</b> <code>/search Into your arms</code>
<b>    Inline:</b> <code>@{BUN} query</code>
<b>    Example:</b> <code>@{BUN} into your arms</code>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Back 🔙", callback_data="cbcmd")
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbdwl"))
async def cbdwl(_, query: CallbackQuery):
    await query.edit_message_text(
        text=f"""
<b><i>Downloading Commands:</b></i>

<b>1. Command:</b> <code>/song song name</code>
<b>    Usage:</b> <code>Downloads requested song from YouTube.</code>
<b>    Example:</b> <code>/song hymn for weekend</code>

<b>2. Command:</b> <code>/video song name</code>
<b>    Usage:</b> <code>Downloads requested video from YouTube.</code>
<b>    Example:</b> <code>/video believer</code>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Back 🔙", callback_data="cbcmd")
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbdelcmds"))
async def cbdelcmds(_, query: CallbackQuery):
    await query.edit_message_text(
        caption=f"""<b><i>Clean Commands:</i></b>

<b>Usage:</b> <code>Deletes the command in your group to avoid spam in your group with bluetexts.</code>
<b>Command:</b> <code>/delcmd on</code> & <code>/delcmd off</code>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Menu 🔙", callback_data="cbhelpmenu")
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbextras"))
async def quotly(_, query: CallbackQuery):
    await query.edit_message_text(
        text=f"""
<b><i>Some Extra Commands:</b></i>

<b>1. Command:</b> <code>/q reply to a message</code> [Normal Quote.]
<b>    Usage:</b> <code>Quotes the given message to sticker.</code>

<b>2. Command:</b> <code>/q (number) reply to a message.</code> [Quotes given number of msgs.]
<b>    Usage:</b> <code>Quotes the given number if messages starting from replied message.</code>
<b>    Example:</b> <code>/q 4 (reply)</code>

<b>3. Command:</b> <code>/q r reply to a message.</code> [Quotes the replied message with it's reply.]
<b>    Usage:</b> <code>Quotes the replied message with along with it's replied message.</code>
<b>    Example:</b> <code>/q r (reply)</code>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Back 🔙", callback_data="cbcmd")
                ]
            ]
        )
    )
