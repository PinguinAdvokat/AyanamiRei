import AiApi
import config
import asyncio
from aiogram import Bot, Dispatcher
from hadlers import ro


bot = Bot(config.TELEGRAM_API)
dp = Dispatcher()


async def start_bot():
    dp.include_router(ro)
    await dp.start_polling(bot)

async def main():
    await asyncio.gather(start_bot())
    


if __name__=="__main__":
    asyncio.run(main())
    
    
