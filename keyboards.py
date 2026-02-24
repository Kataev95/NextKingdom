"""
Клавиатуры с цветными кнопками (Bot API 9.4)
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from config import BUTTON_STYLES, HERO_CLASSES


def get_main_menu() -> ReplyKeyboardMarkup:
    """Главное меню с цветными кнопками"""
    builder = ReplyKeyboardBuilder()
    
    # Первый ряд - основные действия
    builder.button(
        text="⚔️ Профиль",
        style=BUTTON_STYLES["primary"]
    )
    builder.button(
        text="💰 Экономика",
        style=BUTTON_STYLES["success"]
    )
    
    # Второй ряд - боевая система
    builder.button(
        text="🗡️ Битва",
        style=BUTTON_STYLES["danger"]
    )
    builder.button(
        text="🏰 Гильдия",
        style=BUTTON_STYLES["default"]
    )
    
    # Третий ряд - дополнительно
    builder.button(
        text="🗺️ Локации",
        style=BUTTON_STYLES["default"]
    )
    builder.button(
        text="🏆 Рейтинг",
        style=BUTTON_STYLES["default"]
    )
    
    # Четвёртый ряд
    builder.button(
        text="🎯 Квесты",
        style=BUTTON_STYLES["default"]
    )
    builder.button(
        text="📚 Помощь",
        style=BUTTON_STYLES["default"]
    )
    
    builder.adjust(2, 2, 2, 2)
    return builder.as_markup(resize_keyboard=True)


def get_class_selection() -> InlineKeyboardMarkup:
    """Выбор класса героя с цветными кнопками"""
    builder = InlineKeyboardBuilder()
    
    for class_id, class_data in HERO_CLASSES.items():
        builder.button(
            text=f"{class_data['emoji']} {class_data['name']}",
            callback_data=f"class_select:{class_id}",
            style=BUTTON_STYLES["primary"]
        )
    
    builder.adjust(2)
    return builder.as_markup()


def get_economy_menu() -> InlineKeyboardMarkup:
    """Меню экономики"""
    builder = InlineKeyboardBuilder()
    
    # Первый ряд - заработок
    builder.button(
        text="💼 Работать",
        callback_data="economy:work",
        style=BUTTON_STYLES["success"]
    )
    builder.button(
        text="⛏️ Добыча",
        callback_data="economy:mine",
        style=BUTTON_STYLES["success"]
    )
    
    # Второй ряд
    builder.button(
        text="🎁 Ежедневная награда",
        callback_data="economy:daily",
        style=BUTTON_STYLES["primary"]
    )
    
    # Третий ряд
    builder.button(
        text="🏪 Магазин",
        callback_data="shop:main",
        style=BUTTON_STYLES["default"]
    )
    builder.button(
        text="💱 Обмен",
        callback_data="economy:exchange",
        style=BUTTON_STYLES["default"]
    )
    
    # Назад
    builder.button(
        text="◀️ Назад",
        callback_data="back:main",
        style=BUTTON_STYLES["default"]
    )
    
    builder.adjust(2, 1, 2, 1)
    return builder.as_markup()


def get_combat_menu() -> InlineKeyboardMarkup:
    """Меню боевой системы"""
    builder = InlineKeyboardBuilder()
    
    # Первый ряд - PvE
    builder.button(
        text="🐺 Охота на монстров",
        callback_data="combat:hunt",
        style=BUTTON_STYLES["danger"]
    )
    
    # Второй ряд - PvP
    builder.button(
        text="⚔️ Дуэль с игроком",
        callback_data="combat:pvp",
        style=BUTTON_STYLES["danger"]
    )
    
    # Третий ряд - Рейды
    builder.button(
        text="👥 Групповой рейд",
        callback_data="combat:raid",
        style=BUTTON_STYLES["primary"]
    )
    
    # Четвёртый ряд
    builder.button(
        text="🗼 Башня Испытаний",
        callback_data="combat:tower",
        style=BUTTON_STYLES["default"]
    )
    
    # Пятый ряд - Снаряжение
    builder.button(
        text="🛡️ Снаряжение",
        callback_data="equipment:view",
        style=BUTTON_STYLES["default"]
    )
    builder.button(
        text="🎒 Инвентарь",
        callback_data="inventory:view",
        style=BUTTON_STYLES["default"]
    )
    
    # Назад
    builder.button(
        text="◀️ Назад",
        callback_data="back:main",
        style=BUTTON_STYLES["default"]
    )
    
    builder.adjust(1, 1, 1, 1, 2, 1)
    return builder.as_markup()


def get_guild_menu(has_guild: bool = False) -> InlineKeyboardMarkup:
    """Меню гильдии"""
    builder = InlineKeyboardBuilder()
    
    if has_guild:
        # Если игрок в гильдии
        builder.button(
            text="🏰 Информация о гильдии",
            callback_data="guild:info",
            style=BUTTON_STYLES["primary"]
        )
        builder.button(
            text="👥 Участники",
            callback_data="guild:members",
            style=BUTTON_STYLES["default"]
        )
        builder.button(
            text="💰 Казна",
            callback_data="guild:treasury",
            style=BUTTON_STYLES["success"]
        )
        builder.button(
            text="⚔️ Война гильдий",
            callback_data="guild:war",
            style=BUTTON_STYLES["danger"]
        )
        builder.button(
            text="🚪 Покинуть гильдию",
            callback_data="guild:leave",
            style=BUTTON_STYLES["danger"]
        )
    else:
        # Если игрок без гильдии
        builder.button(
            text="➕ Создать гильдию",
            callback_data="guild:create",
            style=BUTTON_STYLES["success"]
        )
        builder.button(
            text="🔍 Найти гильдию",
            callback_data="guild:search",
            style=BUTTON_STYLES["primary"]
        )
        builder.button(
            text="📋 Список гильдий",
            callback_data="guild:list",
            style=BUTTON_STYLES["default"]
        )
    
    # Назад
    builder.button(
        text="◀️ Назад",
        callback_data="back:main",
        style=BUTTON_STYLES["default"]
    )
    
    if has_guild:
        builder.adjust(1, 2, 1, 1, 1)
    else:
        builder.adjust(1, 2, 1)
    
    return builder.as_markup()


def get_shop_menu() -> InlineKeyboardMarkup:
    """Меню магазина"""
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text="⚔️ Оружие",
        callback_data="shop:weapons",
        style=BUTTON_STYLES["default"]
    )
    builder.button(
        text="🛡️ Броня",
        callback_data="shop:armor",
        style=BUTTON_STYLES["default"]
    )
    builder.button(
        text="🧪 Зелья",
        callback_data="shop:potions",
        style=BUTTON_STYLES["success"]
    )
    builder.button(
        text="💎 Особые предметы",
        callback_data="shop:special",
        style=BUTTON_STYLES["primary"]
    )
    
    builder.button(
        text="◀️ Назад",
        callback_data="back:economy",
        style=BUTTON_STYLES["default"]
    )
    
    builder.adjust(2, 2, 1)
    return builder.as_markup()


def get_location_menu() -> InlineKeyboardMarkup:
    """Меню выбора локации"""
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text="🏰 Некстград",
        callback_data="location:nextgrad",
        style=BUTTON_STYLES["success"]
    )
    builder.button(
        text="🌲 Тёмный Лес",
        callback_data="location:dark_forest",
        style=BUTTON_STYLES["danger"]
    )
    builder.button(
        text="🌋 Огненные Горы",
        callback_data="location:fire_mountains",
        style=BUTTON_STYLES["danger"]
    )
    builder.button(
        text="🌿 Изумрудная Долина",
        callback_data="location:emerald_valley",
        style=BUTTON_STYLES["success"]
    )
    builder.button(
        text="❄️ Ледяные Пещеры",
        callback_data="location:ice_caves",
        style=BUTTON_STYLES["primary"]
    )
    builder.button(
        text="🗼 Башня Испытаний",
        callback_data="location:trial_tower",
        style=BUTTON_STYLES["danger"]
    )
    
    builder.button(
        text="◀️ Назад",
        callback_data="back:main",
        style=BUTTON_STYLES["default"]
    )
    
    builder.adjust(2, 2, 2, 1)
    return builder.as_markup()


def get_rating_menu() -> InlineKeyboardMarkup:
    """Меню рейтингов"""
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text="💎 По уровню",
        callback_data="rating:level",
        style=BUTTON_STYLES["primary"]
    )
    builder.button(
        text="💰 По богатству",
        callback_data="rating:coins",
        style=BUTTON_STYLES["success"]
    )
    builder.button(
        text="⚔️ По убийствам",
        callback_data="rating:kills",
        style=BUTTON_STYLES["danger"]
    )
    builder.button(
        text="🏆 По PvP",
        callback_data="rating:pvp",
        style=BUTTON_STYLES["primary"]
    )
    builder.button(
        text="🏰 Рейтинг гильдий",
        callback_data="rating:guilds",
        style=BUTTON_STYLES["default"]
    )
    
    builder.button(
        text="◀️ Назад",
        callback_data="back:main",
        style=BUTTON_STYLES["default"]
    )
    
    builder.adjust(2, 2, 1, 1)
    return builder.as_markup()


def get_monster_selection(player_level: int) -> InlineKeyboardMarkup:
    """Выбор монстра для охоты"""
    from config import MONSTERS
    
    builder = InlineKeyboardBuilder()
    
    for monster_id, monster_data in MONSTERS.items():
        if player_level >= monster_data['level_requirement']:
            builder.button(
                text=f"{monster_data['emoji']} {monster_data['name']} (Ур.{monster_data['level_requirement']})",
                callback_data=f"hunt:{monster_id}",
                style=BUTTON_STYLES["danger"] if monster_data['level_requirement'] >= 10 else BUTTON_STYLES["default"]
            )
    
    builder.button(
        text="◀️ Назад",
        callback_data="back:combat",
        style=BUTTON_STYLES["default"]
    )
    
    builder.adjust(1)
    return builder.as_markup()


def get_confirm_keyboard(action: str) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения действия"""
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text="✅ Да",
        callback_data=f"confirm:{action}:yes",
        style=BUTTON_STYLES["success"]
    )
    builder.button(
        text="❌ Нет",
        callback_data=f"confirm:{action}:no",
        style=BUTTON_STYLES["danger"]
    )
    
    builder.adjust(2)
    return builder.as_markup()


def get_item_actions(item_id: str, item_type: str) -> InlineKeyboardMarkup:
    """Действия с предметом"""
    builder = InlineKeyboardBuilder()
    
    if item_type in ["weapon", "armor", "helmet", "boots", "accessory"]:
        builder.button(
            text="✅ Экипировать",
            callback_data=f"item:equip:{item_id}",
            style=BUTTON_STYLES["success"]
        )
    elif item_type == "potion":
        builder.button(
            text="🧪 Использовать",
            callback_data=f"item:use:{item_id}",
            style=BUTTON_STYLES["success"]
        )
    
    builder.button(
        text="💰 Продать",
        callback_data=f"item:sell:{item_id}",
        style=BUTTON_STYLES["danger"]
    )
    
    builder.button(
        text="◀️ Назад",
        callback_data="inventory:view",
        style=BUTTON_STYLES["default"]
    )
    
    builder.adjust(2, 1, 1)
    return builder.as_markup()


def get_back_button(target: str = "main") -> InlineKeyboardMarkup:
    """Простая кнопка назад"""
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text="◀️ Назад",
        callback_data=f"back:{target}",
        style=BUTTON_STYLES["default"]
    )
    
    return builder.as_markup()