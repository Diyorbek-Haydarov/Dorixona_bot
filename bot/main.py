"""
Main bot initialization and setup
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from .config import BOT_TOKEN, LOG_LEVEL, LOG_FILE
from .database import db
from .handlers import start, search, medicines_list, contact, first_aid, settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    """Main function to start the bot"""
    try:
        # Initialize bot
        bot = Bot(
            token=BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
        )
        
        # Initialize dispatcher with memory storage
        dp = Dispatcher(storage=MemoryStorage())
        
        # Initialize database
        await db.init_db()
        logger.info("Database initialized successfully")
        
        # Register handlers
        dp.include_router(start.router)
        dp.include_router(search.router)
        dp.include_router(medicines_list.router)
        dp.include_router(contact.router)
        dp.include_router(first_aid.router)
        dp.include_router(settings.router)
        
        logger.info("Bot started successfully")
        
        # Start polling
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
