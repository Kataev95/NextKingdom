"""
🏰 NEXT KINGDOM BOT
Полноценная RPG вселенная для Telegram чата The Next

Автор: Amir Inc
Версия: 1.0.0
Python: 3.10+
Framework: aiogram 3.25+
"""

import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TOKEN, CHAT_ID
from handlers import start, economy, combat, guild, admin, events
from database.database import init_db
from utils.scheduler import start_scheduler

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


async def on_startup(bot: Bot):
    """Действия при запуске бота"""
    logger.info("🚀 Next Kingdom Bot запускается...")
    
    # Инициализация базы данных
    await init_db()
    logger.info("✅ База данных инициализирована")
    
    # Запуск планировщика событий
    await start_scheduler(bot, CHAT_ID)  # ✅ Исправлено: добавлен CHAT_ID
    logger.info("⏰ Планировщик событий запущен")
    
    # Уведомление в чат
    startup_message = (
        "🏰 <b>КОРОЛЕВСТВО NEXT ПРОБУЖДАЕТСЯ!</b>\n\n"
        "⚔️ Бот Next Kingdom онлайн и готов к приключениям!\n\n"
        "Используйте /start чтобы начать своё путешествие!\n"
        "Используйте /help для справки по командам."
    )
    
    try:
        await bot.send_message(
            chat_id=CHAT_ID,
            text=startup_message,
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        logger.error(f"Ошибка отправки приветственного сообщения: {e}")
    
    logger.info("✅ Next Kingdom Bot успешно запущен!")


async def on_shutdown(bot: Bot):
    """Действия при остановке бота"""
    logger.info("⏹️ Next Kingdom Bot останавливается...")
    
    shutdown_message = (
        "🌙 <b>Королевство Next засыпает...</b>\n\n"
        "Бот временно оффлайн. Скоро вернёмся!"
    )
    
    try:
        await bot.send_message(
            chat_id=CHAT_ID,
            text=shutdown_message,
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        logger.error(f"Ошибка отправки прощального сообщения: {e}")
    
    logger.info("👋 Next Kingdom Bot остановлен")


async def main():
    """Главная функция запуска бота"""
    
    # Инициализация бота и диспетчера
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )
    
    dp = Dispatcher()
    
    # Регистрация обработчиков (БЕЗ profile.router!)
    dp.include_router(start.router)
    dp.include_router(economy.router)
    dp.include_router(combat.router)
    dp.include_router(guild.router)
    dp.include_router(events.router)
    dp.include_router(admin.router)
    
    # Регистрация startup/shutdown хуков
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Запуск бота
    try:
        logger.info("🎮 Запуск polling...")
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types()
        )
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Фатальная ошибка: {e}")
