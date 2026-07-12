import os
import logging
from logging.handlers import RotatingFileHandler

# Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "6889092713:AAE5Xzb4QISewtSb8-YK7iGS6gdQqJouY3w")

# Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", "38627319"))

# Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "18b0827896e979267ae2251b63830827")

# OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "1327021082"))

# Port
PORT = os.environ.get("PORT", "8080")

# Database 
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://poulomig644_db_user:d9MMUd5PsTP5MDFf@cluster0.q5evcku.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.environ.get("DATABASE_NAME", "Cluster51")

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

# start message
START_MSG = os.environ.get("START_MESSAGE", "<b>Hello {first}!\n\nI am a Website Link Sharing Bot. I can generate unique links for your website slugs.</b>")

try:
    ADMINS = [1327021082]
    for x in (os.environ.get("ADMINS", "1327021082").split()):
        ADMINS.append(int(x))
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")

ADMINS.append(OWNER_ID)
# Remove duplicates
ADMINS = list(set(ADMINS))

LOG_FILE_NAME = "bot.log"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
