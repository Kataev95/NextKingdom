"""
Планировщик событий
"""

import logging
import random
import asyncio
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

from database.database import async_session
from database.models import Player
from sqlalchemy import select

logger = logging.getLogger(__name__)


class EventScheduler:
    """Планировщик случайных событий и задач"""
    
    def __init__(self, bot, chat_id: int):
        self.bot = bot
        self.chat_id = chat_id
        self.scheduler = AsyncIOScheduler()
        logger.info("Планировщик событий инициализирован")
    
    def start(self):
        """Запуск планировщика"""
        # Восстановление энергии каждую минуту
        self.scheduler.add_job(
            self.restore_energy,
            IntervalTrigger(minutes=1),
            id="restore_energy",
            name="Восстановление энергии"
        )
        
        # Случайные события каждые 2-4 часа
        self.scheduler.add_job(
            self.spawn_random_event,
            IntervalTrigger(hours=2),
            id="random_events",
            name="Случайные события"
        )
        
        # Ежедневный сброс в 00:00 UTC
        self.scheduler.add_job(
            self.daily_reset,
            CronTrigger(hour=0, minute=0),
            id="daily_reset",
            name="Ежедневный сброс"
        )
        
        # Очистка истёкших событий каждые 5 минут
        self.scheduler.add_job(
            self.cleanup_events,
            IntervalTrigger(minutes=5),
            id="cleanup_events",
            name="Очистка событий"
        )
        
        # Еженедельный сброс рейтингов (понедельник 00:00)
        self.scheduler.add_job(
            self.weekly_reset,
            CronTrigger(day_of_week='mon', hour=0, minute=0),
            id="weekly_reset",
            name="Еженедельный сброс"
        )
        
        # Уведомление о сервере каждые 6 часов
        self.scheduler.add_job(
            self.server_status,
            IntervalTrigger(hours=6),
            id="server_status",
            name="Статус сервера"
        )
        
        self.scheduler.start()
        logger.info("Планировщик запущен")
    
    def stop(self):
        """Остановка планировщика"""
        self.scheduler.shutdown()
        logger.info("Планировщик остановлен")
    
    async def restore_energy(self):
        """Восстановление энергии всем игрокам"""
        try:
            async with async_session() as session:
                result = await session.execute(select(Player))
                players = result.scalars().all()
                
                updated = 0
                for player in players:
                    if player.energy < player.max_energy:
                        player.energy = min(player.max_energy, player.energy + 1)
                        session.add(player)
                        updated += 1
                
                # Восстановление HP (медленнее - 1 HP каждые 5 минут)
                now = datetime.utcnow()
                if now.minute % 5 == 0:
                    for player in players:
                        if player.hp < player.max_hp:
                            player.hp = min(player.max_hp, player.hp + 5)
                            session.add(player)
                
                await session.commit()
                
                if updated > 0:
                    logger.debug(f"Восстановлена энергия для {updated} игроков")
        
        except Exception as e:
            logger.error(f"Ошибка восстановления энергии: {e}")
    
    async def spawn_random_event(self):
        """Запуск случайного события"""
        try:
            from handlers.events import (
                spawn_meteor_shower,
                spawn_lucky_merchant,
                spawn_happy_hour,
                spawn_boss_raid
            )
            
            events = [
                spawn_meteor_shower,
                spawn_lucky_merchant,
                spawn_happy_hour,
                spawn_boss_raid
            ]
            
            # 30% шанс что событие вообще произойдёт
            if random.random() < 0.3:
                event_func = random.choice(events)
                await event_func(self.bot, self.chat_id)
                logger.info(f"Запущено случайное событие: {event_func.__name__}")
        
        except Exception as e:
            logger.error(f"Ошибка запуска случайного события: {e}")
    
    async def daily_reset(self):
        """Ежедневный сброс"""
        try:
            async with async_session() as session:
                result = await session.execute(select(Player))
                players = result.scalars().all()
                
                for player in players:
                    # Сброс ежедневных лимитов
                    player.daily_work_count = 0
                    player.daily_mine_count = 0
                    session.add(player)
                
                await session.commit()
            
            # Уведомление в чат
            await self.bot.send_message(
                self.chat_id,
                "🌅 <b>НОВЫЙ ДЕНЬ В NEXT KINGDOM!</b>\n\n"
                "Ежедневные лимиты сброшены!\n"
                "Не забудьте забрать ежедневную награду: /daily",
                parse_mode="HTML"
            )
            
            logger.info("Выполнен ежедневный сброс")
        
        except Exception as e:
            logger.error(f"Ошибка ежедневного сброса: {e}")
    
    async def weekly_reset(self):
        """Еженедельный сброс"""
        try:
            async with async_session() as session:
                result = await session.execute(
                    select(Player).order_by(Player.total_coins_earned.desc()).limit(10)
                )
                top_players = result.scalars().all()
                
                # Награждаем топ-10
                rewards = [10000, 7500, 5000, 3000, 2000, 1500, 1000, 750, 500, 250]
                
                winners_text = "🏆 <b>ИТОГИ НЕДЕЛИ</b>\n\n"
                medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
                
                for idx, player in enumerate(top_players):
                    reward = rewards[idx]
                    player.coins += reward
                    player.crystals += (idx == 0) * 100  # Победитель получает 100 кристаллов
                    session.add(player)
                    
                    winners_text += (
                        f"{medals[idx]} <b>{player.first_name}</b>\n"
                        f"   └ Награда: {reward:,} монет\n"
                    )
                
                await session.commit()
            
            # Объявление победителей
            await self.bot.send_message(
                self.chat_id,
                winners_text + "\n🎉 Поздравляем победителей!\n"
                "Новая неделя началась - покажите себя!",
                parse_mode="HTML"
            )
            
            logger.info("Выполнен еженедельный сброс и награждение")
        
        except Exception as e:
            logger.error(f"Ошибка еженедельного сброса: {e}")
    
    async def cleanup_events(self):
        """Очистка истёкших событий"""
        try:
            from handlers.events import cleanup_expired_events
            await cleanup_expired_events()
        except Exception as e:
            logger.error(f"Ошибка очистки событий: {e}")
    
    async def server_status(self):
        """Проверка статуса сервера"""
        try:
            async with async_session() as session:
                from sqlalchemy import func
                result = await session.execute(select(func.count(Player.id)))
                total_players = result.scalar()
            
            # Логируем статус
            logger.info(f"Сервер работает | Игроков: {total_players} | Время: {datetime.utcnow()}")
        
        except Exception as e:
            logger.error(f"Ошибка проверки статуса: {e}")


# Глобальный экземпляр планировщика
_scheduler_instance = None


def get_scheduler(bot, chat_id: int) -> EventScheduler:
    """Получить глобальный экземпляр планировщика"""
    global _scheduler_instance
    
    if _scheduler_instance is None:
        _scheduler_instance = EventScheduler(bot, chat_id)
    
    return _scheduler_instance


async def start_scheduler(bot, chat_id: int):
    """Запустить планировщик"""
    scheduler = get_scheduler(bot, chat_id)
    scheduler.start()
    logger.info("Планировщик событий запущен")


def stop_scheduler():
    """Остановить планировщик"""
    global _scheduler_instance
    
    if _scheduler_instance:
        _scheduler_instance.stop()
        _scheduler_instance = None
        logger.info("Планировщик событий остановлен")