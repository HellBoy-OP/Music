from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from functools import wraps

from .. import hellbot
from ..helper.admins import get_admins
from ..helper.database.db import get_collections
from ..helper.miscs import clog
from .. import client as USER
from ..config import BOT_USERNAME as BUN, OWNER

BOT_PIC = "https://te.legra.ph/file/2a24a198476d4abf505da.jpg"


def admin_check(func):
    @wraps(func)
    async def okvai(hellbot, query):
        admeme = await get_admins(query.message.chat)
        if query.from_user.id == OWNER:
            return await func(hellbot, query)
        elif query.from_user.id in SUDO_USERS:
            return await func(hellbot, query)
        elif query.from_user.id in admeme:
            return await func(hellbot, query)
        else:
            await query.answer("Hmm yes? This is for admins only (⊙_◎)", show_alert=True)
            return
    return okvai


@hellbot.on_callback_query(filters.regex("close"))
async def close(_, query: CallbackQuery):
    await query.message.delete()


@hellbot.on_callback_query(filters.regex("cbback"))
async def cbback(_, query: CallbackQuery):
    await query.edit_message_text(
        text="**Hêllẞø† Control Panel :**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Pause ⏸", callback_data="cbpause"),
                    InlineKeyboardButton("Resume ▶️", callback_data="cbresume")
                ],
                [
                    InlineKeyboardButton("Skip ⏩", callback_data="cbskip"),
                    InlineKeyboardButton("End ⏹", callback_data="cbend")
                ],
                [
                    InlineKeyboardButton("Mute 🔇", callback_data="cbmute"),
                    InlineKeyboardButton("Unmute 🔊", callback_data="cbunmute")
                ],
                [
                    InlineKeyboardButton("Close 🗑️", callback_data="close")
                ]
            ]
        )
    )


@hellbot.on_callback_query(filters.regex("cbstart"))
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


@hellbot.on_callback_query(filters.regex("cbhelpmenu"))
async def cbhelpmenu(_, query: CallbackQuery):
    await query.edit_message_text(
        text=f"""<b><i>Hello there {query.message.from_user.mention} 😉️!</b></i>
<i>Here is the help menu and some basic guide:</i>""",
        reply_markup=InlineKeyboardMarkup([InlineKeyboardButton("How to use ❓", callback_data="cbhowtouse")])
    )


@hellbot.on_callback_query(filters.regex("cbhowtouse"))
async def cbhowtouse(client: hellbot, query: CallbackQuery):
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


@hellbot.on_callback_query(filters.regex("cbcmds"))
async def cbcmds(client: hellbot, query: CallbackQuery):
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


@hellbot.on_callback_query(filters.regex("cbcmd"))
async def cbcmds(client: hellbot, query: CallbackQuery):
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


@hellbot.on_callback_query(filters.regex("cbvc"))
async def cdvc(_, query: CallbackQuery):
    await query.edit_message_text(
        text=f"""<b><i>Voice Chat Command:</b></i>


<b>1. Command:</b> <code>/play</code>
<b>    Usage:</b> <code>Plays the audio in voice chat. If replied to a audio file it'll be played else give a name/link to search and play it from Youtube.</code>
<b>    Example:</b> <code>/play into your arms</code>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Back 🔙", callback_data="cbcmd")
                ]
            ]
        )
    )


@hellbot.on_callback_query(filters.regex("cbadmins"))
async def cbadmins(_, query: CallbackQuery):
    await query.edit_message_text(
        text=f"""<b></i>Admins & Sudo Commands:</b></i>

<b>1. Command:</b> <code>/reload</code>
<b>    Usage:</b> <code>Refresh the list of admins in that group.</code>
<b>    Example:</b> <code>/reload or /admincache</code>

<b>2. Command:</b> <code>/control</code>
<b>    Usage:</b> <code>Opens the control panel with direct access to all controls.</code>
<b>    Example:</b> <code>/control</code>

<b>3. Command:</b> <code>/pause</code>
<b>    Usage:</b> <code>Pauses the music in vouce chat.</code>
<b>    Example:</b> <code>/pause</code>

<b>4. Command:</b> <code>/resume</code>
<b>    Usage:</b> <code>Resumes the paused music in voice chat.</code>
<b>    Example:</b> <code>/resume</code>

<b>5. Command:</b> <code>/end</code>
<b>    Usage:</b> <code>Clears all the songs in queue and leveas the voice chat.</code>
<b>    Example:</b> <code>/end</code>

<b>6. Command:</b> <code>/skip</code>
<b>    Usage:</b> <code>Skips the current song in voive chat.</code>
<b>    Example:</b> <code>/skip</code>

<b>7. Command:</b> <code>/mute</code>
<b>    Usage:</b> <code>Mutes the Voice Chat.</code>
<b>    Example:</b> <code>/mute</code>

<b>8. Command:</b> <code>/unmute</code>
<b>    Usage:</b> <code>Unmute the muted voice chat.</code>
<b>    Example:</b> <code>/unmute</code>

<b>9. Command:</b> <code>/auth</code>
<b>    Usage:</b> <code>Authorises the replied user to use admin commands.</code>
<b>    Example:</b> <code>/auth (reply)</code>

<b>10. Command:</b> <code>/unauth</code>
<b>    Usage:</b> <code>Unauthorises the replied authorised user.</code>
<b>    Example:</b> <code>/unauth (reply)</code>

<b>11. Command:</b> <code>/join</code>
<b>    Usage:</b> <code>Voice Chat Player Account Joins the current group.</code>
<b>    Example:</b> <code>/join</code>

<b>12. Command:</b> <code>/leave</code>
<b>    Usage:</b> <code>Voice Chat Player Account Leaves the current group.</code>
<b>    Example:</b> <code>/leave</code>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Back 🔙", callback_data="cbcmd")
                ]
            ]
        )
    )


@hellbot.on_callback_query(filters.regex("cbothers"))
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

<b>3. Command:</b> <code>/start</code>
<b>    Usage:</b> <code>Get the start message.</code>
<b>    Example:</b> <code>/start</code>

<b>4. Command:</b> <code>/ping</code>
<b>    Usage:</b> <code>Check ping time and uptime of bot.</code>
<b>    Example:</b> <code>/ping</code>

<b>5. Command:</b> <code>/id</code>
<b>    Usage:</b> <code>Fetches the ID.</code>
<b>    Example:</b> <code>/id</code>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Back 🔙", callback_data="cbcmd")
                ]
            ]
        )
    )


@hellbot.on_callback_query(filters.regex("cbdwl"))
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


@hellbot.on_callback_query(filters.regex("cbextras"))
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

<b>4. Command:</b> <code>/delcmd</code>
<b>    Usage:</b> <code>Deletes the command in your group to avoid spam in your group with bluetexts.</code>
<b>    Example:</b> <code>/delcmd (on/off)</code>

<b>5. Command:</b> <code>/lyrics</code>
<b>    Usage:</b> <code>Gets the lyrics of requested song.</code>
<b>    Example:</b> <code>/lyrics perfect</code>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Back 🔙", callback_data="cbcmd")
                ]
            ]
        )
    )
