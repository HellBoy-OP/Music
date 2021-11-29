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
    await query.edit_message_caption(
        caption="**Hêllẞø† Control Panel :**",
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
    await message.reply_photo(
        photo=BOT_PIC,
        caption=f"""
__**Hello!! This is a voice chat music player bot. You can listen to any music using me.**__

**By:** @Its_HellBot
""",
    reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Add in group ✨",
                        url=f"https://t.me/{BUN}?startgroup=true",
                    )
                ],
                [
                    InlineKeyboardButton("How to use ❓", callback_data="cbhowtouse"),
                    InlineKeyboardButton("Commands 📜", callback_data="cbcmds")],
                [
                    InlineKeyboardButton("Deployed By 💝", url=f"tg://openmessage?user_id={OWNER}"),
                ],
                [
                    InlineKeyboardButton(
                        "Group 👥︎", url=f"https://t.me/hellbot_chat"
                    ),
                    InlineKeyboardButton(
                        "Channel 📣", url=f"https://t.me/its_hellbot"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "Repository 💬", url="https://github.com/The-HellBot/Music"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("cbhelpmenu"))
async def cbhelpmenu(_, query: CallbackQuery):
    await query.edit_message_caption(
        caption=f"""<b><i>Hello there {query.message.from_user.mention} 😉️!</b></i>
<i>Here is the help menu and some basic guide:</i>""",
        reply_markup=InlineKeyboardMarkup([InlineKeyboardButton("How to use ❓", callback_data="cbhowtouse")])
    )


@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbhowtouse(_, query: CallbackQuery):
    await query.edit_message_caption(
        caption=f"""<b><i>How to use me?</b></i>

<b>Step 1:</b> <i>Add me( @{BUN} ) and @{(await USER.get_me()).username} in your group or just add me and send /join for automatic joining process.</i>
<b>Step 2:</b> <i>Promote me ( @{BUN} ) and @{(await USER.get_me()).username} with atleast Manage Voice Chat rights.</i>

<i>Done! You are good to go. Now see my command menu to get details of commands I support.</i>

<b><i>By:</b></i> @Its_HellBot""",
        reply_markup=InlineKeyboardMarkup(
            [
                InlineKeyboardButton("Menu 🔙", callback_data="cbhelpmenu"),
                InlineKeyboardButton("Commands 📜", callback_data="cbcmds")
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbgetlyrics"))
async def cbgetlyrics(_, query: CallbackQuery):
    await query.edit_message_caption(
        caption=f"""<b><i>🎶 Lyrics Module:</b></i>

<b>Usage:</b> <code>Gets you the lyrics of given song.</code>
<b>Command:</b> <code>/lyrics song name</code>
<b>Example:</b> <code>/lyrics perfect</code>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Menu 🔙", callback_data="cbhelpmenu"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbytsearch"))
async def cbytsearch(_, query: CallbackQuery):
    await query.edit_message_caption(
        caption=f"""<b><i>Youtube Module:</b></i>

<b>Usage:</b> <code>Searches youtube video in inline mode or via command.</code>

<b>Command:</b> <code>/search query</code>
<b>Example:</b> <code>/search Into your arms</code>

<b>Inline:</b> <code>@{BUN} query</code>
<b>Example:</b> <code>@{BUN} into your arms</code>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Menu 🔙", callback_data="cbhelpmenu"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbmusicdown"))
async def cbmusicdown(_, query: CallbackQuery):
    await query.edit_message_caption(
        caption=f"""<b><i>Song Download Module:</b></i>

<b>Usage:</b> <code>Downloads requested song from YouTube, Deezer, Saavn.</code>

<b>Command:</b> <code>/song song name</code>
<b>Example:</b> <code>/song hymn for weekend</code>

<b>Command:</b> <code>/saavn song name</code>
<b>Example:</b> <code>/saavn believer</code>

<b>Command:</b> <code>/deezer song name</code>
<b>Example:</b> <code>/deezer shape of you</code>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Menu 🔙", callback_data="cbhelpmenu"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbytviddown"))
async def cbytviddown(_, query: CallbackQuery):
    await query.edit_message_caption(
        caption=f"""<b><i>Youtube Video Module:</b></i>

<b>Usage:</b> <code>Downloads the video from youtube.</code>
<b>Command:</b> <code>/video query</code>
<b>Example:</b> <code>/video despacito</code>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Menu 🔙", callback_data="cbhelpmenu"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbdelcmds"))
async def cbdelcmds(_, query: CallbackQuery):
    await query.edit_message_caption(
        caption=f"""<b><i>Clean Commands:</i></b>

<b>Usage:</b> <code>Deletes the command in your group to avoid spam in your group with bluetexts.</code>
<b>Command:</b> <code>/delcmd on</code> & <code>/delcmd off</code>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Menu 🔙", callback_data="cbhelpmenu"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("quotly"))
async def quotly(_, query: CallbackQuery):
    await query.edit_message_caption(
        caption=f"""<b><i>Quotes Module:</b></i>

<b>Usage:</b> <code>Quotes the given message to sticker.</code>

<b>Command:</b> <code>/q reply to a message</code> [Normal Quote.]

<b>Command:</b> <code>/q (number) reply to a message.</code> [Quotes given number of msgs.]
<b>Example:</b> <code>/q 4 (reply)</code>

<b>Command:</b> <code>/q r reply to a message.</code> [Quotes the replied message with it's reply.]
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Menu 🔙", callback_data="cbhelpmenu"
                    )
                ]
            ]
        )
    )
