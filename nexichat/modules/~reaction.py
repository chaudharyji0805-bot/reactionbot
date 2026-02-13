from pyrogram import Client, filters
from pyrogram.types import Message

# yahan apna app import karo
# agar main file ka naam main.py hai:
from main import app
# agar main file ka naam bot.py hai, to upar wali line ko badal ke:
# from bot import app

@app.on_message(filters.incoming)
async def react_to_messages(client: Client, message: Message):
    try:
        await message.react("👍")
    except Exception as e:
        print(f"Failed to react to message: {e}")
