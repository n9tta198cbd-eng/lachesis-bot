"""
Точка входа. Запуск: python run.py
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.config import load_config
from bot.handlers import divination, start
from bot.services.quantum import QRNGOutshiftProvider

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def main() -> None:
    config = load_config()

    bot = Bot(token=config.bot_token)
    dp = Dispatcher()

    quantum = QRNGOutshiftProvider(
        api_key=config.qrng_api_key,
        url=config.qrng_url,
        timeout=config.qrng_timeout,
    )

    dp.include_router(start.router)
    dp.include_router(divination.router)

    logger.info("Lachesis online.")
    await dp.start_polling(bot, allowed_updates=["message", "callback_query"], quantum=quantum)


if __name__ == "__main__":
    asyncio.run(main())
