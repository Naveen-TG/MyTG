from pyrogram import filters
import time, os
from aiohttp import ClientSession
from telegraph import Telegraph
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from telethon import TelegramClient
import logging

OWNER_ID = environ('OWNER_ID' , '')
