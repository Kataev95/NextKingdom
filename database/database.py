"""
Инициализация и работа с базой данных
"""

import logging
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select

from config import DATABASE_URL
from database.models import Base, Player, Guild, Achievement

logger = logging.getLogger(__name__)

# Создание движка базы данных
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Установи True для отладки SQL запросов
)

# Фабрика сессий
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    """Инициализация базы данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("✅ База данных инициализирована")
    
    # Добавление базовых достижений
    await init_achievements()


async def init_achievements():
    """Инициализация базовых достижений"""
    achievements_data = [
        {
            "achievement_id": "first_blood",
            "name": "Первая кровь",
            "description": "Убейте первого монстра",
            "reward_coins": 100,
            "reward_crystals": 1,
            "reward_exp": 50,
            "icon": "🩸"
        },
        {
            "achievement_id": "hunter",
            "name": "Охотник",
            "description": "Убейте 100 монстров",
            "reward_coins": 1000,
            "reward_crystals": 5,
            "reward_exp": 500,
            "icon": "🏹"
        },
        {
            "achievement_id": "first_coins",
            "name": "Первые деньги",
            "description": "Заработайте 1000 монет",
            "reward_coins": 500,
            "reward_crystals": 2,
            "reward_exp": 100,
            "icon": "💰"
        },
        {
            "achievement_id": "rich",
            "name": "Богач",
            "description": "Накопите 100,000 монет",
            "reward_coins": 10000,
            "reward_crystals": 10,
            "reward_exp": 1000,
            "icon": "💎"
        },
        {
            "achievement_id": "gladiator",
            "name": "Гладиатор",
            "description": "Выиграйте 10 PvP дуэлей",
            "reward_coins": 2000,
            "reward_crystals": 5,
            "reward_exp": 750,
            "icon": "⚔️"
        },
        {
            "achievement_id": "guild_leader",
            "name": "Лидер",
            "description": "Создайте гильдию",
            "reward_coins": 5000,
            "reward_crystals": 10,
            "reward_exp": 1000,
            "icon": "👑"
        },
        {
            "achievement_id": "explorer",
            "name": "Путешественник",
            "description": "Посетите все локации",
            "reward_coins": 3000,
            "reward_crystals": 7,
            "reward_exp": 800,
            "icon": "🗺️"
        },
        {
            "achievement_id": "level_10",
            "name": "Опытный герой",
            "description": "Достигните 10 уровня",
            "reward_coins": 1000,
            "reward_crystals": 3,
            "reward_exp": 0,
            "icon": "⭐"
        },
        {
            "achievement_id": "level_25",
            "name": "Ветеран",
            "description": "Достигните 25 уровня",
            "reward_coins": 5000,
            "reward_crystals": 10,
            "reward_exp": 0,
            "icon": "⭐⭐"
        },
        {
            "achievement_id": "level_50",
            "name": "Мастер",
            "description": "Достигните 50 уровня",
            "reward_coins": 20000,
            "reward_crystals": 25,
            "reward_exp": 0,
            "icon": "⭐⭐⭐"
        }
    ]
    
    async with async_session() as session:
        for ach_data in achievements_data:
            # Проверяем, существует ли достижение
            result = await session.execute(
                select(Achievement).where(Achievement.achievement_id == ach_data["achievement_id"])
            )
            existing = result.scalar_one_or_none()
            
            if not existing:
                achievement = Achievement(**ach_data)
                session.add(achievement)
        
        await session.commit()
    
    logger.info("✅ Базовые достижения добавлены")


async def get_player(user_id: int) -> Player | None:
    """Получить игрока из базы"""
    async with async_session() as session:
        result = await session.execute(
            select(Player).where(Player.id == user_id)
        )
        return result.scalar_one_or_none()


async def create_player(user_id: int, username: str | None, first_name: str, hero_class: str) -> Player:
    """Создать нового игрока"""
    from config import HERO_CLASSES, START_COINS, START_LEVEL, START_HP, START_ENERGY
    from datetime import datetime
    
    class_data = HERO_CLASSES.get(hero_class, HERO_CLASSES["warrior"])
    
    player = Player(
        id=user_id,
        username=username,
        first_name=first_name,
        hero_class=hero_class,
        level=START_LEVEL,
        exp=0,
        exp_needed=100,
        coins=START_COINS,
        crystals=0,
        power_shards=0,
        hp=START_HP + class_data["hp_bonus"],
        max_hp=START_HP + class_data["hp_bonus"],
        energy=START_ENERGY,
        max_energy=START_ENERGY,
        strength=class_data["strength"] * 2,
        agility=class_data["agility"] * 2,
        intelligence=class_data["intelligence"] * 2,
        defense=5,
        current_location="nextgrad",
        created_at=datetime.utcnow(),
        last_active=datetime.utcnow()
    )
    
    async with async_session() as session:
        session.add(player)
        await session.commit()
        await session.refresh(player)
    
    logger.info(f"✅ Создан новый игрок: {first_name} (ID: {user_id}, Класс: {hero_class})")
    return player


async def update_player(player: Player):
    """Обновить данные игрока"""
    from datetime import datetime
    
    player.last_active = datetime.utcnow()
    
    async with async_session() as session:
        session.add(player)
        await session.commit()


async def get_top_players(order_by: str = "level", limit: int = 10):
    """Получить топ игроков"""
    from sqlalchemy import desc
    
    async with async_session() as session:
        if order_by == "level":
            result = await session.execute(
                select(Player).order_by(desc(Player.level), desc(Player.exp)).limit(limit)
            )
        elif order_by == "coins":
            result = await session.execute(
                select(Player).order_by(desc(Player.coins)).limit(limit)
            )
        elif order_by == "kills":
            result = await session.execute(
                select(Player).order_by(desc(Player.total_monsters_killed)).limit(limit)
            )
        elif order_by == "pvp":
            result = await session.execute(
                select(Player).order_by(desc(Player.total_pvp_wins)).limit(limit)
            )
        else:
            result = await session.execute(
                select(Player).order_by(desc(Player.level)).limit(limit)
            )
        
        return result.scalars().all()