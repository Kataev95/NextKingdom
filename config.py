"""
Конфигурация Next Kingdom Bot
"""

import os
from dotenv import load_dotenv

load_dotenv()

# === ОСНОВНЫЕ НАСТРОЙКИ ===
TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
CHAT_ID = int(os.getenv("CHAT_ID", "-1002132913097"))  # ID чата The Next

# === БАЗА ДАННЫХ ===
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///next_kingdom.db")

# === ИГРОВЫЕ НАСТРОЙКИ ===

# Стартовые значения
START_COINS = 1000
START_LEVEL = 1
START_HP = 100
START_ENERGY = 100

# Экономика
WORK_COOLDOWN = 3600  # 1 час
WORK_REWARD_MIN = 100
WORK_REWARD_MAX = 300

DAILY_COOLDOWN = 86400  # 24 часа
DAILY_REWARD = 500
DAILY_STREAK_BONUS = 100  # За каждый день подряд

MINE_COOLDOWN = 7200  # 2 часа
MINE_REWARD_MIN = 150
MINE_REWARD_MAX = 500

# Боевая система
HUNT_COOLDOWN = 1800  # 30 минут
HUNT_ENERGY_COST = 20
PVP_ENERGY_COST = 30
PVP_COOLDOWN = 600  # 10 минут

ENERGY_REGEN_RATE = 1  # 1 энергия в минуту
ENERGY_MAX = 100

# Уровни и опыт
EXP_BASE = 100  # Базовый опыт для 2 уровня
EXP_MULTIPLIER = 1.5  # Множитель роста опыта

# Гильдии
GUILD_CREATE_COST = 10000
GUILD_MAX_MEMBERS = 20
GUILD_WAR_COOLDOWN = 604800  # 7 дней

# Рейтинги
TOP_DISPLAY_COUNT = 10

# === КЛАССЫ ГЕРОЕВ ===
HERO_CLASSES = {
    "warrior": {
        "name": "⚔️ Воин",
        "emoji": "⚔️",
        "strength": 5,
        "agility": 3,
        "intelligence": 2,
        "hp_bonus": 50,
        "description": "Мастер ближнего боя с высоким уроном"
    },
    "archer": {
        "name": "🏹 Лучник",
        "emoji": "🏹",
        "strength": 3,
        "agility": 5,
        "intelligence": 3,
        "hp_bonus": 30,
        "description": "Специалист дальнего боя и критических ударов"
    },
    "mage": {
        "name": "🔮 Маг",
        "emoji": "🔮",
        "strength": 2,
        "agility": 2,
        "intelligence": 5,
        "hp_bonus": 20,
        "description": "Повелитель магии и заклинаний"
    },
    "assassin": {
        "name": "🗡️ Убийца",
        "emoji": "🗡️",
        "strength": 3,
        "agility": 5,
        "intelligence": 3,
        "hp_bonus": 25,
        "description": "Мастер скрытности и мгновенных убийств"
    },
    "paladin": {
        "name": "🛡️ Паладин",
        "emoji": "🛡️",
        "strength": 4,
        "agility": 2,
        "intelligence": 4,
        "hp_bonus": 60,
        "description": "Защитник и целитель"
    },
    "merchant": {
        "name": "💰 Торговец",
        "emoji": "💰",
        "strength": 2,
        "agility": 3,
        "intelligence": 4,
        "hp_bonus": 15,
        "description": "Эксперт экономики и торговли"
    }
}

# === МОНСТРЫ ===
MONSTERS = {
    "goblin": {
        "name": "Гоблин",
        "emoji": "👺",
        "hp": 50,
        "damage": 10,
        "defense": 5,
        "exp_reward": 20,
        "coins_reward": (30, 80),
        "level_requirement": 1
    },
    "wolf": {
        "name": "Волк",
        "emoji": "🐺",
        "hp": 80,
        "damage": 15,
        "defense": 8,
        "exp_reward": 35,
        "coins_reward": (50, 120),
        "level_requirement": 3
    },
    "orc": {
        "name": "Орк",
        "emoji": "👹",
        "hp": 120,
        "damage": 20,
        "defense": 15,
        "exp_reward": 50,
        "coins_reward": (80, 200),
        "level_requirement": 5
    },
    "troll": {
        "name": "Тролль",
        "emoji": "👿",
        "hp": 200,
        "damage": 30,
        "defense": 25,
        "exp_reward": 80,
        "coins_reward": (150, 350),
        "level_requirement": 10
    },
    "dragon": {
        "name": "Дракон",
        "emoji": "🐉",
        "hp": 500,
        "damage": 60,
        "defense": 40,
        "exp_reward": 200,
        "coins_reward": (500, 1000),
        "level_requirement": 20
    },
    "dark_knight": {
        "name": "Тёмный Рыцарь",
        "emoji": "⚔️",
        "hp": 350,
        "damage": 45,
        "defense": 35,
        "exp_reward": 150,
        "coins_reward": (300, 600),
        "level_requirement": 15
    }
}

# === ПРЕДМЕТЫ ===
ITEMS = {
    # Оружие
    "wooden_sword": {
        "name": "Деревянный меч",
        "type": "weapon",
        "rarity": "common",
        "damage": 5,
        "price": 100,
        "level_req": 1
    },
    "iron_sword": {
        "name": "Железный меч",
        "type": "weapon",
        "rarity": "uncommon",
        "damage": 15,
        "price": 500,
        "level_req": 5
    },
    "steel_sword": {
        "name": "Стальной меч",
        "type": "weapon",
        "rarity": "rare",
        "damage": 30,
        "price": 2000,
        "level_req": 10
    },
    "legendary_blade": {
        "name": "Легендарный клинок",
        "type": "weapon",
        "rarity": "legendary",
        "damage": 100,
        "price": 50000,
        "level_req": 30
    },
    
    # Броня
    "leather_armor": {
        "name": "Кожаная броня",
        "type": "armor",
        "rarity": "common",
        "defense": 5,
        "price": 150,
        "level_req": 1
    },
    "iron_armor": {
        "name": "Железная броня",
        "type": "armor",
        "rarity": "uncommon",
        "defense": 15,
        "price": 600,
        "level_req": 5
    },
    "steel_armor": {
        "name": "Стальная броня",
        "type": "armor",
        "rarity": "rare",
        "defense": 35,
        "price": 2500,
        "level_req": 10
    },
    
    # Зелья
    "small_hp_potion": {
        "name": "Малое зелье здоровья",
        "type": "potion",
        "rarity": "common",
        "heal": 50,
        "price": 50,
        "level_req": 1
    },
    "medium_hp_potion": {
        "name": "Среднее зелье здоровья",
        "type": "potion",
        "rarity": "uncommon",
        "heal": 100,
        "price": 150,
        "level_req": 5
    },
    "large_hp_potion": {
        "name": "Большое зелье здоровья",
        "type": "potion",
        "rarity": "rare",
        "heal": 200,
        "price": 400,
        "level_req": 10
    }
}

# Редкости предметов
RARITY_COLORS = {
    "common": "⚪",
    "uncommon": "🟢",
    "rare": "🔵",
    "epic": "🟣",
    "legendary": "🟡",
    "mythic": "🔴"
}

RARITY_MULTIPLIER = {
    "common": 1.0,
    "uncommon": 1.1,
    "rare": 1.25,
    "epic": 1.5,
    "legendary": 2.0,
    "mythic": 3.0
}

# === СОБЫТИЯ ===
RANDOM_EVENTS = {
    "meteor_shower": {
        "name": "🌟 Метеоритный дождь",
        "description": "С неба падают метеориты! Первые 10 человек получают награду!",
        "reward_coins": 500,
        "reward_exp": 100,
        "duration": 300,  # 5 минут
        "max_participants": 10
    },
    "lucky_merchant": {
        "name": "🎁 Удачливый торговец",
        "description": "В городе появился торговец со скидками 50%!",
        "discount": 0.5,
        "duration": 600  # 10 минут
    },
    "happy_hour": {
        "name": "⚡ Счастливый час",
        "description": "Все награды удвоены на следующий час!",
        "multiplier": 2.0,
        "duration": 3600  # 1 час
    },
    "boss_raid": {
        "name": "💀 Нашествие боссов",
        "description": "Мощный босс атакует город! Объединитесь для победы!",
        "boss_hp": 5000,
        "boss_damage": 40,
        "reward_coins": 2000,
        "reward_exp": 500,
        "duration": 1800  # 30 минут
    }
}

# Шанс появления случайного события (проверка каждый час)
EVENT_SPAWN_CHANCE = 0.3  # 30%

# === ЦВЕТНЫЕ КНОПКИ (Bot API 9.4) ===
BUTTON_STYLES = {
    "primary": "primary",    # 🔵 Синяя
    "success": "success",    # 🟢 Зелёная
    "danger": "danger",      # 🔴 Красная
    "default": None          # ⚪ Обычная
}

# === ЭМОДЗИ ИКОНКИ ДЛЯ КНОПОК ===
BUTTON_EMOJIS = {
    "sword": "5310076249404621168",
    "shield": "5285430309720966085",
    "coin": "5285032475490273112",
    "gem": "5373141891321699086",
    "fire": "5314467653763017659",
    "star": "5314467653763017659"
}

# === АДМИНИСТРАТОРЫ ===
ADMINS = [
    8492109371,  # Замени на свой Telegram ID
]

# === ВРЕМЕННЫЕ ЗОНЫ И СОБЫТИЯ ===
WEEKLY_EVENTS = {
    0: "trade_day",      # Понедельник
    1: "hunt_day",       # Вторник
    2: "guild_day",      # Среда
    3: "pvp_day",        # Четверг
    4: "chaos_night",    # Пятница
    5: "tower_day",      # Суббота
    6: "rest_day"        # Воскресенье
}

# === ЛОКАЦИИ ===
LOCATIONS = {
    "nextgrad": {
        "name": "🏰 Некстград",
        "description": "Столица королевства",
        "emoji": "🏰"
    },
    "dark_forest": {
        "name": "🌲 Тёмный Лес",
        "description": "Опасное место с монстрами",
        "emoji": "🌲",
        "danger_level": 2
    },
    "fire_mountains": {
        "name": "🌋 Огненные Горы",
        "description": "Вулканический регион",
        "emoji": "🌋",
        "danger_level": 4
    },
    "emerald_valley": {
        "name": "🌿 Изумрудная Долина",
        "description": "Мирное место",
        "emoji": "🌿",
        "danger_level": 1
    },
    "ice_caves": {
        "name": "❄️ Ледяные Пещеры",
        "description": "Загадочные пещеры",
        "emoji": "❄️",
        "danger_level": 3
    },
    "trial_tower": {
        "name": "🗼 Башня Испытаний",
        "description": "100 этажей испытаний",
        "emoji": "🗼",
        "danger_level": 5
    }
}
# ============================
# АДМИН-ДОСТУП
# ============================

# Твой Telegram ID для админ-команд
# Получи свой ID от бота @userinfobot
ADMIN_IDS = [
    8492109371,  # Замени на свой реальный ID
]
