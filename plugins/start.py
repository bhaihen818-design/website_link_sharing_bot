import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, START_MSG
from database.database import add_user, del_user, full_userbase, present_user
from datetime import datetime

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
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

@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    if not await present_user(user_id):
        await add_user(user_id)

    if len(message.text) > 7:
        from database.link_db import get_link_by_token
        token = message.text.split(" ", 1)[1]
        link_data = await get_link_by_token(token)
        
        if link_data:
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("🌐 Open Website", url=link_data['url'])]
            ])
            return await message.reply_text(
                f"<b>Welcome!</b>\n\nYou can access the content by clicking the button below.",
                reply_markup=reply_markup,
                quote=True
            )
        else:
            return await message.reply("<b>Invalid Link</b>", quote=True)

    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("About Me", callback_data="about"),
          InlineKeyboardButton("Close", callback_data="close")]]
    )
    await message.reply_text(
        text=START_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=reply_markup,
        disable_web_page_preview=True,
        quote=True
    )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    users = await full_userbase()
    await message.reply(f"{len(users)} users are using this bot")

@Bot.on_message(filters.command('stats') & filters.private & filters.user(ADMINS))
async def stats_handler(client: Bot, message: Message):
    now = datetime.now()
    delta = now - client.uptime
    time = get_readable_time(delta.seconds)
    await message.reply(f"<b>Bot Uptime:</b> {time}")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def broadcast_handler(client: Bot, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply to a message to broadcast it.")
    
    query = await full_userbase()
    broadcast_msg = message.reply_to_message
    total, successful, blocked, deleted, unsuccessful = 0, 0, 0, 0, 0
    
    pls_wait = await message.reply("<i>Broadcast processing...</i>")
    for chat_id in query:
        try:
            await broadcast_msg.copy(chat_id)
            successful += 1
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await broadcast_msg.copy(chat_id)
            successful += 1
        except UserIsBlocked:
            await del_user(chat_id)
            blocked += 1
        except InputUserDeactivated:
            await del_user(chat_id)
            deleted += 1
        except Exception:
            unsuccessful += 1
        total += 1
    
    status = f"""<b><u>Broadcast Completed</u>
    
Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
    
    await pls_wait.edit(status)
