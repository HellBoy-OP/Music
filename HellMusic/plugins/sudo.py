import io
import os
import re
import sys
import traceback
import subprocess
from pyrogram import filters
from pyrogram.types import Message
from HellMusic.plugins import BOT_UN
from HellMusic import SUDO_USERS, bot, trg
from HellMusic.core.client import client_id
from HellMusic.helpers.error import parse_error


@bot.on_message(
    filters.command(["eval", f"eval@{BOT_UN}"], prefixes=trg) & filters.user(SUDO_USERS)
)
async def eval(bot, message: Message):
    hell = await message.reply_text("Processing ...")
    lists = message.text.split(" ", 1)
    if len(lists) != 2:
        return await parse_error(hell, "Received empty message!")
    reply = message.reply_to_message
    hell_id, _, hell_mention = await client_id(message)
    cmd = lists[1].strip()
    reply_to = message.reply_to_message or message

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, bot, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = "<b>EVAL</b>: "
    final_output += f"<code>{cmd}</code>\n\n"
    final_output += "<b>OUTPUT</b>:\n"
    final_output += f"<code>{evaluation.strip()}</code> \n"
    if len(final_output) > 4096:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.txt"
            await reply_to.reply_document(
                document=out_file, caption=cmd[:1000], disable_notification=True
            )
    else:
        await reply_to.reply_text(final_output)
    await hell.delete()


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


@bot.on_message(
    filters.command(["term", f"term@{BOT_UN}"], prefixes=trg) & filters.user(SUDO_USERS)
)
async def term(bot, message: Message):
    hell = await message.reply_text("Processing ...")
    lists = message.text.split(" ", 1)
    if len(lists) != 2:
        return await parse_error(hell, "Received empty message!")
    reply = message.reply_to_message
    cmd = lists[1].strip()
    reply_to = message.reply_to_message or message
    if "\n" in cmd:
        code = cmd.split("\n")
        output = ""
        for x in code:
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
            try:
                process = subprocess.Popen(
                    shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
            except Exception as err:
                print(err)
                await hell.edit(f"**Error:** \n`{err}`")
            output += f"**{code}**\n"
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", cmd)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type, value=exc_obj, tb=exc_tb
            )
            await hell.edit("**Error:**\n`{}`".format("".join(errors)))
            return
        output = process.stdout.read()[:-1].decode("utf-8")
    if str(output) == "\n":
        output = None
    if output:
        if len(output) > 4096:
            filename = "output.txt"
            with open(filename, "w+") as file:
                file.write(output)
            await message.reply_document(
                filename,
                caption=f"`{cmd}`",
            )
            os.remove(filename)
            return
        await hell.edit(f"**Output:**\n`{output}`")
    else:
        await hell.edit("**Output:**\n`No Output`")
