import asyncio
from start import nexichat, sudo  # start file se import

async def main():
    sudo()
    bot = nexichat  # start file me already `nexichat = nexichat()`
    await bot.start()
    print(f"Bot started as @{bot.username} ({bot.id})")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
