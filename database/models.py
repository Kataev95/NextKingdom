"""
Модели базы данных для Next Kingdom
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, Integer, String, DateTime, Boolean, Float, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Player(Base):
    """Модель игрока"""
    __tablename__ = "players"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)  # Telegram ID
    username: Mapped[Optional[str]] = mapped_column(String(100))
    first_name: Mapped[str] = mapped_column(String(100))
    
    # Прогресс
    level: Mapped[int] = mapped_column(Integer, default=1)
    exp: Mapped[int] = mapped_column(Integer, default=0)
    exp_needed: Mapped[int] = mapped_column(Integer, default=100)
    
    # Ресурсы
    coins: Mapped[int] = mapped_column(Integer, default=1000)
    crystals: Mapped[int] = mapped_column(Integer, default=0)
    power_shards: Mapped[int] = mapped_column(Integer, default=0)
    
    # Характеристики
    hp: Mapped[int] = mapped_column(Integer, default=100)
    max_hp: Mapped[int] = mapped_column(Integer, default=100)
    energy: Mapped[int] = mapped_column(Integer, default=100)
    max_energy: Mapped[int] = mapped_column(Integer, default=100)
    
    strength: Mapped[int] = mapped_column(Integer, default=10)
    agility: Mapped[int] = mapped_column(Integer, default=10)
    intelligence: Mapped[int] = mapped_column(Integer, default=10)
    defense: Mapped[int] = mapped_column(Integer, default=5)
    
    # Класс героя
    hero_class: Mapped[str] = mapped_column(String(50), default="warrior")
    
    # Локация
    current_location: Mapped[str] = mapped_column(String(50), default="nextgrad")
    
    # Статистика
    total_monsters_killed: Mapped[int] = mapped_column(Integer, default=0)
    total_pvp_wins: Mapped[int] = mapped_column(Integer, default=0)
    total_pvp_losses: Mapped[int] = mapped_column(Integer, default=0)
    total_coins_earned: Mapped[int] = mapped_column(Integer, default=0)
    
    # Кулдауны
    last_work: Mapped[Optional[datetime]] = mapped_column(DateTime)
    last_daily: Mapped[Optional[datetime]] = mapped_column(DateTime)
    last_mine: Mapped[Optional[datetime]] = mapped_column(DateTime)
    last_hunt: Mapped[Optional[datetime]] = mapped_column(DateTime)
    last_pvp: Mapped[Optional[datetime]] = mapped_column(DateTime)
    daily_streak: Mapped[int] = mapped_column(Integer, default=0)
    
    # Гильдия
    guild_id: Mapped[Optional[int]] = mapped_column(ForeignKey("guilds.id"))
    guild_role: Mapped[str] = mapped_column(String(20), default="member")  # member, officer, leader
    
    # Даты
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_active: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Связи
    inventory: Mapped[list["Inventory"]] = relationship(back_populates="player", cascade="all, delete-orphan")
    equipment: Mapped[list["Equipment"]] = relationship(back_populates="player", cascade="all, delete-orphan")
    guild: Mapped[Optional["Guild"]] = relationship(back_populates="members")
    achievements: Mapped[list["PlayerAchievement"]] = relationship(back_populates="player", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Player {self.first_name} (Lv.{self.level})>"


class Guild(Base):
    """Модель гильдии"""
    __tablename__ = "guilds"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    leader_id: Mapped[int] = mapped_column(BigInteger)
    
    # Ресурсы гильдии
    treasury: Mapped[int] = mapped_column(Integer, default=0)
    level: Mapped[int] = mapped_column(Integer, default=1)
    exp: Mapped[int] = mapped_column(Integer, default=0)
    
    # Статистика
    total_members: Mapped[int] = mapped_column(Integer, default=1)
    wars_won: Mapped[int] = mapped_column(Integer, default=0)
    wars_lost: Mapped[int] = mapped_column(Integer, default=0)
    
    # Даты
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_war: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    # Связи
    members: Mapped[list["Player"]] = relationship(back_populates="guild")
    
    def __repr__(self):
        return f"<Guild {self.name} (Lv.{self.level})>"


class Inventory(Base):
    """Инвентарь игрока"""
    __tablename__ = "inventory"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("players.id"))
    
    item_id: Mapped[str] = mapped_column(String(50))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    
    obtained_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Связи
    player: Mapped["Player"] = relationship(back_populates="inventory")
    
    def __repr__(self):
        return f"<Inventory {self.item_id} x{self.quantity}>"


class Equipment(Base):
    """Экипированные предметы"""
    __tablename__ = "equipment"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("players.id"))
    
    slot: Mapped[str] = mapped_column(String(20))  # weapon, armor, helmet, boots, accessory
    item_id: Mapped[str] = mapped_column(String(50))
    
    equipped_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Связи
    player: Mapped["Player"] = relationship(back_populates="equipment")
    
    def __repr__(self):
        return f"<Equipment {self.slot}: {self.item_id}>"


class Achievement(Base):
    """Достижения"""
    __tablename__ = "achievements"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    achievement_id: Mapped[str] = mapped_column(String(50), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    
    reward_coins: Mapped[int] = mapped_column(Integer, default=0)
    reward_crystals: Mapped[int] = mapped_column(Integer, default=0)
    reward_exp: Mapped[int] = mapped_column(Integer, default=0)
    
    icon: Mapped[str] = mapped_column(String(10))
    
    # Связи
    players: Mapped[list["PlayerAchievement"]] = relationship(back_populates="achievement")
    
    def __repr__(self):
        return f"<Achievement {self.name}>"


class PlayerAchievement(Base):
    """Достижения игрока"""
    __tablename__ = "player_achievements"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("players.id"))
    achievement_id: Mapped[int] = mapped_column(Integer, ForeignKey("achievements.id"))
    
    unlocked_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Связи
    player: Mapped["Player"] = relationship(back_populates="achievements")
    achievement: Mapped["Achievement"] = relationship(back_populates="players")
    
    def __repr__(self):
        return f"<PlayerAchievement {self.player_id} -> {self.achievement_id}>"


class ActiveEvent(Base):
    """Активные события"""
    __tablename__ = "active_events"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_type: Mapped[str] = mapped_column(String(50))
    
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ends_at: Mapped[datetime] = mapped_column(DateTime)
    
    data: Mapped[Optional[str]] = mapped_column(Text)  # JSON для хранения доп. данных
    participants: Mapped[Optional[str]] = mapped_column(Text)  # JSON список участников
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    def __repr__(self):
        return f"<ActiveEvent {self.event_type}>"


class Transaction(Base):
    """История транзакций"""
    __tablename__ = "transactions"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    player_id: Mapped[int] = mapped_column(BigInteger)
    
    transaction_type: Mapped[str] = mapped_column(String(50))  # work, daily, purchase, etc
    amount: Mapped[int] = mapped_column(Integer)
    currency: Mapped[str] = mapped_column(String(20))  # coins, crystals, shards
    
    description: Mapped[str] = mapped_column(String(255))
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Transaction {self.transaction_type}: {self.amount}>"


class BattleLog(Base):
    """Логи сражений"""
    __tablename__ = "battle_logs"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    attacker_id: Mapped[int] = mapped_column(BigInteger)
    defender_id: Mapped[Optional[int]] = mapped_column(BigInteger)  # Null если PvE
    
    battle_type: Mapped[str] = mapped_column(String(20))  # pve, pvp
    winner_id: Mapped[int] = mapped_column(BigInteger)
    
    attacker_damage: Mapped[int] = mapped_column(Integer)
    defender_damage: Mapped[int] = mapped_column(Integer)
    
    rewards: Mapped[Optional[str]] = mapped_column(Text)  # JSON
    
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<BattleLog {self.battle_type}: {self.attacker_id} vs {self.defender_id}>"