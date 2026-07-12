# Website Link Sharing Bot

A lightweight, fast, and production-ready Telegram bot to generate and share unique website links with slugs.

## Features

- **Website Settings:** Configure a base website URL via `/setweb`.
- **Link Generation:** Generate unique Telegram start links for specific website slugs via `/genlink`.
- **Token Resolution:** Automatically resolve tokens from Telegram start links and provide a direct button to the website.
- **Admin System:** Manage users, broadcast messages, and view bot stats.
- **Asynchronous:** Built with Pyrogram and Motor (Async MongoDB) for maximum performance.

## Commands

### Admin Commands
- `/setweb <url>` - Set the base website URL.
- `/getweb` - View the current base website URL.
- `/genlink <slug>` - Generate a Telegram link for a specific slug.
- `/users` - View the total number of users.
- `/stats` - View bot uptime.
- `/broadcast` - Broadcast a message to all users (reply to a message).

### User Commands
- `/start` - Start the bot.
- `/start <token>` - Access the website link associated with the token.

## Setup

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Set environment variables:
   - `TG_BOT_TOKEN`: Your Telegram bot token.
   - `APP_ID`: Your Telegram App ID.
   - `API_HASH`: Your Telegram API Hash.
   - `DATABASE_URL`: Your MongoDB connection URI.
   - `DATABASE_NAME`: Your MongoDB database name.
   - `ADMINS`: List of admin user IDs (space-separated).
4. Run the bot: `python main.py`.

## Credits
Modified by Manus AI.
