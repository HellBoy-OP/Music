from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery
from functools import wraps

from ..config import OWNER


def owner_check(func):
    @wraps(func)
    async def okvai(message, query):
        if query.from_user.id == OWNER:
            return await func(message, query)
        else:
            await query.answer("Hmm yes? This is for owner only (⊙_◎)", show_alert=True)
            return
    return okvai


OWNER_HELPCB = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "Tools 🔧", callback_data="cbownertools"
            )
        ],
        [
            InlineKeyboardButton(
                "Help Menu 📜", callback_data="cbhelpmenu"
            )
        ]
    ]
)


@Client.on_callback_query(filters.regex("cbownertools"))
@owner_check
async def cbtools(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b><i>Owner Control Panel:</b></i>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Bans ⛔", callback_data="cbbans"
                    ),
                    InlineKeyboardButton(
                        "Unbans 🍀", callback_data="cbunbans"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Stats 📊", callback_data="cbuserstats"
                    ),
                    InlineKeyboardButton(
                        "Broadcast 💬", callback_data="cbbroadcast"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbbans"))
@owner_check
async def cbbans(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b><i>Ban Moment:</b></i>

<b><i>Usage:</b></i> <code>Bans the user from using this bot.</code>
<b><i>Command:</b></i> <code>/ban userid reason</code>
<b><i>Example:</b></i> <code>/ban 69696969 nice</code>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Menu 🔙", callback_data="cbownertools"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbunbans"))
@owner_check
async def cbunbans(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b><i>Unban Moment:</b></i>

<b><i>Usage:</i></b> <code>Unbans the banned user and allows them to use me.</code>
<b><i>Command:</b></i> <code>/unban userid</code>
<b><i>Example:</b></i> <code>/unban 6969696</code>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Menu 🔙", callback_data="cbownertools"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbuserstats"))
@owner_check
async def cbuserstats(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b><i>Stats Moment:</i></b>

<b><i>Usage:</b></i> <code>Statistics keeper of this bot.</code>
<b><i>Command:</b></i> <code>/stats</code>
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Menu 🔙", callback_data="cbownertools"
                    )
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("cbbroadcast"))
@owner_check
async def cbbroadcast(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""<b><i>Broadcast Moment:</i></b>

<b><i>Usage:</i></b> <code>Broadcast a message to all the users of this bot.</code>

<b><i>Command:</b></i> <code>/fbroadcast (reply to a message)</code> [Broadcast as a forward message.]

<b><i>Command:</b></i> <code>/broadcast (reply to a message)</code> [Broadcast without forward tag.]

<b><i>Command:</b></i> <code>/gcast (reply to a message)</code> [Broadcast from assistant account.]
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Menu 🔙", callback_data="cbownertools"
                    )
                ]
            ]
        )
    )


@Client.on_message(filters.command("ownerpanel") & filters.user(OWNER) & ~filters.edited)
async def modhelp(_, message: Message):
    txt = "<b><i>Hello!! This is Owner Panel. Some owner only commands are explained here.</b></i>"
    await message.reply_text(txt, reply_markup=OWNER_HELPCB)
