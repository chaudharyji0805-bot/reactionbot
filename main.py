import asyncio
from pyrogram import Client

# Bot config
BOT_TOKEN = "PASTE_YOUR_BOT_TOKEN"
API_ID = 123456       # apna daal
API_HASH = "YOUR_API_HASH"

app = Client(
    "reaction_bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

async def main():
    await app.start()
    print("Bot started successfully!")
    await asyncio.Event().wait()  # keep bot alive

if __name__ == "__main__":
    asyncio.run(main())
