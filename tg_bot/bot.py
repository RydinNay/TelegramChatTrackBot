# tg_bot/bot.py
import asyncio
from tg_bot.bot_instance import bot, dp
from tg_bot.handlers.main_command import main_command_router
from tg_bot.handlers.report_handlers import report_command_router

dp.include_router(main_command_router)
dp.include_router(report_command_router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
