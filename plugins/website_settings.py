from pyrogram import Client, filters
from pyrogram.types import Message
from bot import Bot
from config import ADMINS
from database.link_db import set_website_url, get_website_url

@Bot.on_message(filters.command('setweb') & filters.private & filters.user(ADMINS))
async def set_web_handler(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: /setweb https://example.com")
    
    url = message.command[1]
    if not url.startswith(("http://", "https://")):
        return await message.reply("Invalid URL. Must start with http:// or https://")
    
    # Remove trailing slash for consistency
    url = url.rstrip("/")
    
    await set_website_url(url)
    await message.reply(f"Website URL set to: {url}")

@Bot.on_message(filters.command('getweb') & filters.private & filters.user(ADMINS))
async def get_web_handler(client: Client, message: Message):
    url = await get_website_url()
    if url:
        await message.reply(f"Current Website URL: {url}")
    else:
        await message.reply("No website URL configured. Use /setweb to set one.")
