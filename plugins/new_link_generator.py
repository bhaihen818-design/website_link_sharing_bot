import random
import string
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS
from database.link_db import get_website_url, add_link, get_link_by_slug

def generate_random_token(length=12):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@Bot.on_message(filters.command('genlink') & filters.private & filters.user(ADMINS))
async def genlink_handler(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: /genlink Slug\nExample: /genlink Naruto")
    
    slug = message.command[1]
    
    # Check if website URL is configured
    website_url = await get_website_url()
    if not website_url:
        return await message.reply("Website URL not configured. Use /setweb first.")
    
    # Check if slug already exists
    existing_link = await get_link_by_slug(slug)
    if existing_link:
        link = f"https://t.me/{client.username}?start={existing_link['token']}"
        return await message.reply(f"Slug already exists!\n\nExisting Link: {link}")
    
    # Generate unique token
    token = generate_random_token()
    
    # Full URL for the button
    full_url = f"{website_url}/{slug}"
    
    # Store in DB
    await add_link(token, slug, full_url, message.from_user.id)
    
    # Generate start link
    start_link = f"https://t.me/{client.username}?start={token}"
    
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={start_link}')]
    ])
    
    await message.reply_text(
        f"<b>✅ Link Generated!</b>\n\n"
        f"<b>Slug:</b> <code>{slug}</code>\n"
        f"<b>Target URL:</b> {full_url}\n\n"
        f"<b>Telegram Link:</b>\n{start_link}",
        reply_markup=reply_markup,
        quote=True
    )
