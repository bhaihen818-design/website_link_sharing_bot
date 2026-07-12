import os
import logging
from logging.handlers import RotatingFileHandler

# Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

# Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", "22505271"))

# Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "c89a94fcfda4bc06524d0903977fc81e")

# OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "6695586027"))

# Port
PORT = os.environ.get("PORT", "8080")

# Database 
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://Cluster0:Cluster0@cluster0.c07xkuf.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DATABASE_NAME", "Cluster01")

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

# start message
START_MSG = os.environ.get("START_MESSAGE", "<b>Hello {first}!\n\nI am a Website Link Sharing Bot. I can generate unique links for your website slugs.</b>")

try:
    ADMINS = [6695586027]
    for x in (os.environ.get("ADMINS", "6695586027").split()):
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
