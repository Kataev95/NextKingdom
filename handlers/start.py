"""
Обработчик команд старта и выбора класса
"""

import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.enums import ParseMode

from database.database import get_player, create_player
from keyboards import get_main_menu, get_class_selection
from config import HERO_CLASSES, LOCATIONS

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Команда /start - регистрация или возврат игрока"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    
    # Проверяем, зарегистрирован ли игрок
    player = await get_player(user_id)
    
    if player:
        # Игрок уже зарегистрирован
        welcome_back_text = (
            f"🏰 <b>С возвращением в Королевство Next, {player.first_name}!</b>\n\n"
            f"⚔️ <b>Ваш герой:</b>\n"
            f"└ {HERO_CLASSES[player.hero_class]['emoji']} {HERO_CLASSES[player.hero_class]['name']}\n"
            f"└ Уровень: {player.level}\n"
            f"└ 💰 Монеты: {player.coins:,}\n"
            f"└ 💎 Кристаллы: {player.crystals}\n\n"
            f"📍 <b>Текущая локация:</b> {LOCATIONS[player.current_location]['emoji']} {LOCATIONS[player.current_location]['name']}\n\n"
            f"Используйте меню ниже для навигации!"
        )
        
        await message.answer(
            welcome_back_text,
            reply_markup=get_main_menu(),
            parse_mode=ParseMode.HTML
        )
        
        logger.info(f"Вернулся игрок: {first_name} (ID: {user_id})")
    else:
        # Новый игрок - начало регистрации
        intro_text = (
            "🏰 <b>ДОБРО ПОЖАЛОВАТЬ В КОРОЛЕВСТВО NEXT!</b>\n\n"
            "📖 <i>Легенда гласит...</i>\n\n"
            "Тысячи лет назад великий маг <b>Некст Основатель</b> создал это королевство, "
            "используя силу <b>Кристалла Бесконечности</b>. Но <b>Тёмный Лорд Хаос</b> "
            "стремится захватить кристалл и поработить все земли.\n\n"
            "Перед смертью Некст Основатель разделил силу кристалла на фрагменты "
            "и спрятал их по всему королевству.\n\n"
            "🔥 <b>Ты — один из новых героев!</b>\n"
            "Собери все фрагменты, победи Тёмного Лорда и спаси королевство!\n\n"
            "⚔️ Но сначала выбери свой путь героя..."
        )
        
        await message.answer(
            intro_text,
            parse_mode=ParseMode.HTML
        )
        
        await message.answer(
            "🎭 <b>Выберите класс героя:</b>\n\n"
            "Каждый класс обладает уникальными характеристиками и способностями!",
            reply_markup=get_class_selection(),
            parse_mode=ParseMode.HTML
        )
        
        logger.info(f"Новый игрок начал регистрацию: {first_name} (ID: {user_id})")


@router.callback_query(F.data.startswith("class_select:"))
async def process_class_selection(callback: CallbackQuery):
    """Обработка выбора класса"""
    class_id = callback.data.split(":")[1]
    
    if class_id not in HERO_CLASSES:
        await callback.answer("❌ Неверный класс!", show_alert=True)
        return
    
    user_id = callback.from_user.id
    username = callback.from_user.username
    first_name = callback.from_user.first_name
    
    # Проверяем, не зарегистрирован ли уже
    player = await get_player(user_id)
    if player:
        await callback.answer("Вы уже зарегистрированы!", show_alert=True)
        return
    
    # Создаём игрока
    class_data = HERO_CLASSES[class_id]
    player = await create_player(user_id, username, first_name, class_id)
    
    # Красивое сообщение о создании персонажа
    creation_text = (
        f"✨ <b>ГЕРОЙ СОЗДАН!</b> ✨\n\n"
        f"🎭 <b>Класс:</b> {class_data['emoji']} {class_data['name']}\n"
        f"📝 <i>{class_data['description']}</i>\n\n"
        f"📊 <b>Характеристики:</b>\n"
        f"└ 💪 Сила: {class_data['strength']*2}\n"
        f"└ 🏃 Ловкость: {class_data['agility']*2}\n"
        f"└ 🧠 Интеллект: {class_data['intelligence']*2}\n"
        f"└ 🛡️ Защита: 5\n"
        f"└ ❤️ Здоровье: {player.max_hp}\n"
        f"└ ⚡ Энергия: {player.max_energy}\n\n"
        f"💰 <b>Стартовый капитал:</b> {player.coins:,} монет\n\n"
        f"🏰 <b>Локация:</b> {LOCATIONS['nextgrad']['emoji']} Некстград\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎮 <b>НАЧИНАЕМ ПРИКЛЮЧЕНИЕ!</b>\n\n"
        f"Используйте меню ниже для навигации.\n"
        f"Команда /help покажет список всех команд."
    )
    
    await callback.message.edit_text(
        creation_text,
        parse_mode=ParseMode.HTML
    )
    
    await callback.message.answer(
        "🏰 <b>Главное меню:</b>",
        reply_markup=get_main_menu(),
        parse_mode=ParseMode.HTML
    )
    
    await callback.answer("✅ Персонаж создан!")
    
    logger.info(f"Создан персонаж: {first_name} - {class_data['name']} (ID: {user_id})")


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Команда /help - справка"""
    help_text = (
        "📚 <b>СПРАВКА ПО КОМАНДАМ</b>\n\n"
        
        "🎮 <b>ОСНОВНЫЕ КОМАНДЫ:</b>\n"
        "/start - Начать игру / Вернуться\n"
        "/profile - Ваш профиль\n"
        "/help - Эта справка\n\n"
        
        "💰 <b>ЭКОНОМИКА:</b>\n"
        "/work - Работать (1 час кд)\n"
        "/daily - Ежедневная награда\n"
        "/mine - Добыча ресурсов (2 часа кд)\n"
        "/shop - Магазин предметов\n"
        "/balance - Проверить баланс\n\n"
        
        "⚔️ <b>БИТВЫ:</b>\n"
        "/hunt - Охота на монстров\n"
        "/pvp @username - Дуэль с игроком\n"
        "/raid - Групповой рейд\n"
        "/tower - Башня Испытаний\n\n"
        
        "🏰 <b>ГИЛЬДИЯ:</b>\n"
        "/guild - Меню гильдии\n"
        "/guild_create - Создать гильдию\n"
        "/guild_info - Информация о гильдии\n"
        "/guild_leave - Покинуть гильдию\n\n"
        
        "📊 <b>ИНФОРМАЦИЯ:</b>\n"
        "/stats - Ваша статистика\n"
        "/inventory - Инвентарь\n"
        "/equipment - Снаряжение\n"
        "/top - Рейтинги игроков\n"
        "/location - Текущая локация\n\n"
        
        "🎯 <b>ПРОЧЕЕ:</b>\n"
        "/quest - Доступные квесты\n"
        "/achievements - Достижения\n"
        "/events - Активные события\n\n"
        
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💡 <b>СОВЕТЫ:</b>\n"
        "• Используйте кнопки меню для удобства\n"
        "• Выполняйте /daily каждый день\n"
        "• Прокачивайте снаряжение\n"
        "• Вступайте в гильдии\n"
        "• Участвуйте в событиях\n\n"
        
        "🎮 <b>Удачных приключений в Next Kingdom!</b>"
    )
    
    await message.answer(help_text, parse_mode=ParseMode.HTML)


@router.message(Command("profile"))
async def cmd_profile(message: Message):
    """Команда /profile - профиль игрока"""
    user_id = message.from_user.id
    player = await get_player(user_id)
    
    if not player:
        await message.answer(
            "❌ Вы не зарегистрированы! Используйте /start",
            parse_mode=ParseMode.HTML
        )
        return
    
    # Вычисляем ранг
    if player.level < 10:
        rank = "🥉 Бронза"
    elif player.level < 25:
        rank = "🥈 Серебро"
    elif player.level < 50:
        rank = "🥇 Золото"
    elif player.level < 75:
        rank = "💎 Платина"
    else:
        rank = "👑 Мастер"
    
    # Прогресс до следующего уровня
    exp_progress = (player.exp / player.exp_needed) * 100
    progress_bar = "█" * int(exp_progress / 10) + "░" * (10 - int(exp_progress / 10))
    
    class_data = HERO_CLASSES[player.hero_class]
    location = LOCATIONS[player.current_location]
    
    profile_text = (
        f"⚔️ <b>ПРОФИЛЬ ГЕРОЯ</b>\n\n"
        
        f"👤 <b>{player.first_name}</b>\n"
        f"{'@' + player.username if player.username else ''}\\n\n"
        
        f"🎭 <b>Класс:</b> {class_data['emoji']} {class_data['name']}\n"
        f"🏆 <b>Ранг:</b> {rank}\n"
        f"📊 <b>Уровень:</b> {player.level}\n\n"
        
        f"✨ <b>Опыт:</b> {player.exp:,} / {player.exp_needed:,}\n"
        f"[{progress_bar}] {exp_progress:.1f}%\n\n"
        
        f"💰 <b>РЕСУРСЫ:</b>\n"
        f"└ ⭐ Next Coins: {player.coins:,}\n"
        f"└ 💎 Кристаллы: {player.crystals}\n"
        f"└ 🔥 Осколки Силы: {player.power_shards}\n\n"
        
        f"📊 <b>ХАРАКТЕРИСТИКИ:</b>\n"
        f"└ ❤️ HP: {player.hp}/{player.max_hp}\n"
        f"└ ⚡ Энергия: {player.energy}/{player.max_energy}\n"
        f"└ 💪 Сила: {player.strength}\n"
        f"└ 🏃 Ловкость: {player.agility}\n"
        f"└ 🧠 Интеллект: {player.intelligence}\n"
        f"└ 🛡️ Защита: {player.defense}\n\n"
        
        f"📍 <b>Локация:</b> {location['emoji']} {location['name']}\n\n"
        
        f"📈 <b>СТАТИСТИКА:</b>\n"
        f"└ 💀 Убито монстров: {player.total_monsters_killed}\n"
        f"└ ⚔️ Побед в PvP: {player.total_pvp_wins}\n"
        f"└ 💔 Поражений в PvP: {player.total_pvp_losses}\n"
        f"└ 💰 Заработано монет: {player.total_coins_earned:,}\n\n"
        
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎮 <i>Продолжайте приключение!</i>"
    )
    
    await message.answer(profile_text, parse_mode=ParseMode.HTML)
    logger.info(f"Просмотр профиля: {player.first_name} (ID: {user_id})")