from requests import post, get
import os
import aiofiles
import requests 
import socket
from asyncio import get_running_loop
from functools import partial
from info import ADMINS as dev_user
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.types import Message
from pyrogram import Client as bot
from SafoneAPI import SafoneAPI

Safone = SafoneAPI()

from plugins.xtra.http import post as send

BASE = "https://batbin.me/"
    
      
def spacebin(text):
    url = "https://spaceb.in/api/v1/documents/"
    res = post(url, data={"content": text, "extension": "txt"})
    return f"https://spaceb.in/{res.json()['payload']['id']}"


def _netcat(host, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    while True:
        data = s.recv(4096).decode("utf-8").strip("\n\x00")
        if not data:
            break
        return data
    s.close()
    
async def ezup(content):
    loop = get_running_loop()
    link = await loop.run_in_executor(
        None, partial(_netcat, "ezup.dev", 9999, content)
    )
    return link


@bot.on_message(filters.command("batbin"))
async def pastebin(_, m):
          if m.reply_to_message:
              content = m.reply_to_message.text or m.reply_to_message.caption
              
              button = [[ InlineKeyboardButton(text="BATBIN", url=link)]]
              await m.reply_photo(photo=link,caption=link,reply_markup=InlineKeyboardMarkup(button))

@bot.on_message(filters.command("shizu"))
async def shizuki(_, m):
          if m.reply_to_message:
              content = m.reply_to_message.text or m.reply_to_message.caption
              link = await Safone.paste(content)
              button = [[ InlineKeyboardButton(text="Shizu", url=link)]]
              await m.reply_text(link,reply_markup=InlineKeyboardMarkup(button))

@bot.on_message(filters.command('paste'))
async def paste(_, m):
 try:
    reply = m.reply_to_message
    if not reply:
           await m.reply_text("Reply to Message or Text-File")
    if reply.document:
        doc = await m.reply_to_message.download()
        async with aiofiles.open(doc, mode="r") as f:
          file_text = await f.read()
        os.remove(doc)
        msg = await m.reply("**Starting to Paste in All Bins**")
        spacebin_url = spacebin(file_text)
        ezup_link = await ezup(file_text)
        resp = await send(f"{BASE}api/v2/paste", data=file_text)
        code = resp["message"]
        bat_link = f"{BASE}{code}"
        await msg.edit("**Process Completed**")                  
        caption = f"Here is the Paste Hubs of @VijayFilterTG_BoT"
        await m.reply_photo(photo=bat_link,caption=caption,
                      reply_markup=InlineKeyboardMarkup(
                          [[InlineKeyboardButton(text="BATBIN", url=bat_link),InlineKeyboardButton("SPACEBIN", url=spacebin_url),
                         ],[ InlineKeyboardButton("EZUPBIN", url=ezup_link)]]))
    elif reply.text or reply.caption:
          text = reply.text or reply.caption
          msg = await m.reply("**Starting to Paste in All Bins**")                
          spacebin_url = spacebin(text)
          link = await ezup(text)
          resp = await send(f"{BASE}api/v2/paste", data=text)
          code = resp["message"]
          bat_link = f"{BASE}{code}"
          await msg.edit("**Process Completed**")                 
          caption = f"Here are the Paste Webs of Requested Paste"
          await m.reply_photo(photo=bat_link,caption=caption,
                      reply_markup=InlineKeyboardMarkup(
                          [[InlineKeyboardButton(text="BATBIN", url=bat_link)],[ InlineKeyboardButton("SPACEBIN", url=spacebin_url),
                           ],[ InlineKeyboardButton("EZUP.DEV", url=link)]]))
    
        
        

 except Exception as e:
       await m.reply(f"**ERROR**: {e}")
