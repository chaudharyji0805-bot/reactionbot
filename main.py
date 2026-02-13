import asyncio

# ---- Python 3.11 + Pyrogram fix ----
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except Exception:
    pass

try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
# -----------------------------------

import logging
import time
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
import config

# Logging
logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

logging.getLogger("pyrogram").setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)

# Mongo
mongodb_async = MongoCli(config.MONGO_URL)
db_async = mongodb_async.Anonymous

mongo_sync = MongoClient(config.MONGO_URL)
mongodb = mongo_sync.VIP

OWNER = config.OWNER_ID

SUDOERS = filters.user()

def sudo():
    global SUDOERS
    OWNER_ID = config.OWNER_ID
    if config.MONGO_URL is None:
        SUDOERS.add(OWNER_ID)
    else:
        sudoersdb = mongodb.sudoers
        sudoers = sudoersdb.find_one({"sudo": "sudo"})
        sudoers = [] if not sudoers else sudoers["sudoers"]
        SUDOERS.add(OWNER_ID)
        if OWNER_ID not in sudoers:
            sudoers.append(OWNER_ID)
            sudoersdb.update_one(
                {"sudo": "sudo"},
                {"$set": {"sudoers": sudoers}},
                upsert=True,
            )
        if sudoers:
            for x in sudoers:
                SUDOERS.add(x)
    print("Sudoers Loaded.")

class nexichat(Client):
    def __init__(self):
        super().__init__(
            name="nexichat",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.DEFAULT,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.username = self.me.username
        LOGGER.info("Bot started as %s", self.username)

    async def stop(self):
        await super().stop()
        LOGGER.info("Bot stopped")

# Init
sudo()
app = nexichat()

async def main():
    await app.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
