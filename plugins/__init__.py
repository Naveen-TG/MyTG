from os import environ
from pyrogram import filters
import time, os
from aiohttp import ClientSession
from telegraph import Telegraph
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from telethon import TelegramClient
import logging

OWNER_ID = environ.get('OWNER_ID', '2107036689')
DEV_USERS = environ.get('DEV_USERS', '2107036689')


tbot = TelegramClient("Dhanush", API_ID, API_HASH)
