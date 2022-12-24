 from info import DATABASE_URI as mongodb
from pyrogram import Client as bot
from pyrogram import filters
from pyrogram.types import *
from pyrogram.enums import ChatType



usersdb = mongodb.users

async def is_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True

async def get_users() -> list:
    users_list = []
    async for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list
    
async def add_user(user_id: int):
    is_served = await is_user(user_id)
    if is_served:
        return
    return await usersdb.insert_one({"user_id": user_id})   

 
##################### GROUPS DB #####################
chatsdb = mongodb.chats

async def is_group(chat: int) -> bool:
    group = await chatsdb.find_one({"chat": chat})
    if not group:
        return False
    return True

async def get_groups() -> list:
    groups_list = []
    async for chat in chatsdb.find({"chat": {"$gt": 0}}):
        groups_list.append(chat)
    return groups_list
    
async def add_group(chat: int):
    is_served = await is_group(chat)
    if is_served:
        return
    return await chatsdb.insert_one({"chat": chat})   

NEW_USER_TEXT = """**Someone Started Our Bot ヘ(^_^)ヘ**

**🕵 Name: {}**
**🆔 UID: {}**

**🌟 Total UserStats: {}**
"""
START_TEXT = """ **Hey? {}
Do you know I can do anything for you? (๑•́ ₃ •̀๑) check my available commands for /help.**
"""


## Written by @NandhaxD ##

START_BTN = [[ InlineKeyboardButton(text="🆘", callback_data="help_back"),
InlineKeyboardButton(text="📊", url="t.me/Nandha_Network"),],[ InlineKeyboardButton(text="SUPPORT", url="NandhaSupport.t.me"),InlineKeyboardButton(text="UPDATES", url="Nandhabots.t.me")]]


@bot.on_message(filters.command("start",["/","!",".","?","$"]))
async def start(_, message):
     user_id = message.from_user.id
     mention = message.from_user.mention
     if message.chat.type == ChatType.PRIVATE and not await is_user(user_id):
            await add_user(user_id)
            mention = message.from_user.mention
            id = message.from_user.id
            user_stats = len(await get_users())
            await bot.send_message(-1001717881477, text=NEW_USER_TEXT.format(mention, id, user_stats))
            await message.reply_text(START_TEXT.format(mention),reply_markup=InlineKeyboardMarkup(START_BTN))
            return 
         
     elif message.chat.type == ChatType.PRIVATE and await is_user(user_id):

               return await message.reply_text(START_TEXT.format(mention),reply_markup=InlineKeyboardMarkup(START_BTN))
     elif message.chat.type == ChatType.SUPERGROUP or ChatType.GROUP:
            return await message.reply_text("**I'm Already Awake! Nani yo?\n\n    ¯\_(ツ)_/¯**")
        
                                            
NEW_GROUP = """**New Group Added Our Bot**!

👥 **Group Name: {}**

📊 **Total Groups: {}**
"""

@bot.on_message(filters.command("addgroup"))
async def addgroup(_, m):
       chat = str(m.chat.id).replace("-100", "")
       await add_group(chat)
       await m.reply("**New group added")

@bot.on_message(filters.new_chat_members)
async def new_chat(_, message):
    chat = str(message.chat.id).replace("-100", "")
    bot_id = (await bot.get_me()).id
    await add_group(chat)
    for member in message.new_chat_members:
        if member.id == bot_id:
            await message.reply(
                "😘 Thanks for add me to your group ! "
            )
            a = message.chat.title
            b = len(await get_groups())
            await bot.send_message(
                 -1001717881477,
                 NEW_GROUP.format(a,b)
            )                                                                                    
                                            
