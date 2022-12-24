import io
import sys
import io
import os
import glob
import textwrap
from contextlib import redirect_stdout
from telethon.sync import events
import time
import pyrogram
StartTime = time.time()
import traceback
from subprocess import getoutput as run
from plugins.xtra.utils.dbfunctions import add_sudo, remove_sudo, get_sudoers
from plugins.stats import get_users, get_groups
from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from requests import post

from plugins import dev_user
from plugins import OWNER_ID
from pyrogram import Client as app
from plugins import tbot


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time
                  
@bot.on_message(filters.command(["rsudo","removesudo"]))
async def removesudo(_, message):
            if not message.reply_to_message:
                   return await message.reply("**Reply to Someone.**")
            elif message.from_user.id in dev_user and not message.reply_to_message.from_user.id in (await get_sudoers()):
                   return await message.reply("**The User is Not Sudo**.")
            elif message.from_user.id in dev_user:
                   
                  msg = await message.reply("**Removeing. Sudo**")
                  mention = (await bot.get_users(message.reply_to_message.from_user.id)).mention
                  await remove_sudo(message.reply_to_message.from_user.id)
                  await msg.edit(f"**Successfully Removed Sudo {mention}**")
           
@bot.on_message(filters.command(["getsudos","sudolist"]))
async def sudolist(_, message):
           if message.from_user.id not in dev_user or not message.from_user.id in (await get_sudoers()):
                 return await message.reply("**Only Rank Users Can Access**")
           else:
                  user_ids = (await get_sudoers())
                  sudo_text = ""
                  for name in user_ids:
                           ok = await bot.get_users(user_ids)
                           sudo_text = f"**• {ok.mention}**"
                  await message.reply(sudo_text)

@bot.on_message(filters.command(["addsudo","addsupport"]))
async def addsudo(_, message):
            if not message.reply_to_message:
                   return await message.reply("**Reply to Someone.**")
            elif message.from_user.id in dev_user and message.reply_to_message.from_user.id in (await get_sudoers()):
                   return await message.reply("**The User is Already Sudo**.")
            elif message.from_user.id in dev_user:
                   
                  msg = await message.reply("**Adding. Sudo**")
                  mention = (await bot.get_users(message.reply_to_message.from_user.id)).mention
                  await add_sudo(message.reply_to_message.from_user.id)
                  await msg.edit(f"**Successfully Added Sudo {mention}**")
           
@bot.on_message(filters.command('devlist'))
async def devlist(_, m):
      if m.from_user.id in dev_user:
         DEV_TXT = ""
         for dev in dev_user:
                   name = await bot.get_users(dev)
                   DEV_TXT += f"• **{name.mention}**\n"
         await m.reply(DEV_TXT)
      else:
          m.reply("only Devs can access this command!")
  
        
@app.on_message(filters.command("sh", prefixes=['/', '.', '?', '-']))
def sh(_, m):
    if m.from_user.id in dev_user:
        code = m.text.replace(m.text.split(" ")[0], "")
        x = run(code)
        m.reply(
            f"**SHELL**: `{code}`\n\n**OUTPUT**:\n`{x}`")
    else:
        m.reply("only Devs can access this command!")


@app.on_message(filters.command("stats") & filters.user(dev_user))
async def stats(_, message):
        path = "nandhabot/plugins/*.py"
        files = glob.glob(path)
        text = f"**Total Plugins:** `{len(files)}`\n"
        text += f"**Total Users:** `{len(await get_users())}`\n"
        text += f"**Total Groups:** `{len(await get_groups())}`"
        await message.reply_text(text)

@app.on_message(filters.command("listmodules") & filters.user(dev_user))
async def listmodules(_, message):
            path = "nandhabot/plugins/*.py"
            files = glob.glob(path)
            module_list = "Total Plugins List:\n"
            for name in files:
                   lmao = name.replace(".py", "")
                   k = lmao.replace("nandhabot/plugins/", "")
                   module_list +=  f"{k}\n"
            msg = await message.reply("**Document Process.**")
            with io.BytesIO(str.encode(module_list)) as file:
                   file.name = "moduleslist.txt"
                   await msg.edit("**Process Complete.**")
                   await message.reply_document(
                      document=file, caption="**List loaded plugins**") 
            
          
def paste(text):
    url = "https://spaceb.in/api/v1/documents/"
    res = post(url, data={"content": text, "extension": "txt"})
    return f"https://spaceb.in/{res.json()['payload']['id']}"


@bot.on_message(
    filters.command("logs", prefixes=[".", "/", ";", "," "*"]) & filters.user(dev_user)
)
def sendlogs(_, m: Message):
    logs = run("tail logs.txt")
    x = paste(logs)
    keyb = [
        [
            InlineKeyboardButton("Link", url=x),
            InlineKeyboardButton("File", callback_data="sendfile"),
        ],
    ]
    m.reply(x, disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(keyb))



@bot.on_callback_query(filters.regex(r"sendfile"))
def sendfilecallback(_, query: CallbackQuery):
    sender = query.from_user.id
    query.message.chat.id

    if sender in dev_user:
        query.message.edit("`Sending...`")
        query.message.reply_document("logs.txt")

    else:
        query.answer(
            "This Is A Developer's Restricted Command.You Don't Have Access To Use This."
        )
      
@app.on_message(filters.user(dev_user) & filters.command("eval"))
async def eval(client, message):
    status_message = await message.reply_text("Processing ...")
    cmd = message.text.split(" ", maxsplit=1)[1]

    reply_to_ = message
    if message.reply_to_message:
        reply_to_ = message.reply_to_message

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, message)
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
            out_file.name = "eval.text"
            await reply_to_.reply_document(
                document=out_file, caption=cmd, disable_notification=True
            )
    else:
        await reply_to_.reply_text(final_output)
    await status_message.delete()


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)

@app.on_message(filters.user(dev_user) & filters.command("ping", prefixes=['/', '.', '?', '-']))
async def ping(_, m):
    start_time = time.time()
    img = "https://telegra.ph/file/fb6a277156b2956f26aa1.jpg"
    end_time = time.time()
    ping_time = round((end_time - start_time) * 1000, 3)
    uptime = get_readable_time((time.time() - StartTime))
    ping_message = await m.reply_text("Processing ...")
    await m.reply_photo(photo=img, caption=f"**🏓 PONG!!:** `{ping_time} ms`\n**🆙 UPTIME:** `{uptime}`")
    await ping_message.delete()
    
