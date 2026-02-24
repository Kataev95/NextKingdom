"""
Обработчик экономических команд
"""

import logging
import random
from datetime import datetime, timedelta
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.enums import ParseMode

from database.database import get_player, update_player
from keyboards import get_economy_menu, get_back_button
from config import (
    WORK_COOLDOWN, WORK_REWARD_MIN, WORK_REWARD_MAX,
    DAILY_COOLDOWN, DAILY_REWARD, DAILY_STREAK_BONUS,
    MINE_COOLDOWN, MINE_REWARD_MIN, MINE_REWARD_MAX
)

router = Router()
logger = logging.getLogger(__name__)


def check_cooldown(last_time: datetime | None, cooldown_seconds: int) -> tuple[bool, int]:
    """Проверка кулдауна"""
    if not last_time:
        return True, 0
    
    now = datetime.utcnow()
    time_passed = (now - last_time).total_seconds()
    
    if time_passed >= cooldown_seconds:
        return True, 0
    else:
        remaining = int(cooldown_seconds - time_passed)
        return False, remaining


def format_time(seconds: int) -> str:
    """Форматирование времени"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}ч {minutes}м {secs}с"
    elif minutes > 0:
        return f"{minutes}м {secs}с"
    else:
        return f"{secs}с"


@router.message(Command("work"))
async def cmd_work(message: Message):
    """Команда /work - работа за монеты"""
    user_id = message.from_user.id
    player = await get_player(user_id)
    
    if not player:
        await message.answer("❌ Вы не зарегистрированы! Используйте /start")
        return
    
    # Проверка кулдауна
    can_work, remaining = check_cooldown(player.last_work, WORK_COOLDOWN)
    
    if not can_work:
        await message.answer(
            f"⏰ <b>Вы уже работали недавно!</b>\n\n"
            f"Следующая работа доступна через: {format_time(remaining)}",
            parse_mode=ParseMode.HTML
        )
        return
    
    # Награда за работу
    reward = random.randint(WORK_REWARD_MIN, WORK_REWARD_MAX)
    
    # Бонус для торговца
    if player.hero_class == "merchant":
        reward = int(reward * 1.5)
    
    player.coins += reward
    player.total_coins_earned += reward
    player.last_work = datetime.utcnow()
    
    await update_player(player)
    
    # Случайные сообщения о работе
    work_messages = [
        "🔨 Вы поработали на строительстве городских стен!",
        "📦 Вы помогли разгрузить торговые повозки!",
        "⚒️ Вы добывали руду в шахтах!",
        "🌾 Вы помогали собирать урожай!",
        "🛡️ Вы стояли на страже города!",
        "📚 Вы переписывали древние манускрипты!",
        "🐴 Вы ухаживали за королевскими лошадьми!"
    ]
    
    work_text = (
        f"{random.choice(work_messages)}\n\n"
        f"💰 <b>Заработано:</b> +{reward:,} Next Coins\n"
        f"💼 <b>Ваш баланс:</b> {player.coins:,} NC\n\n"
        f"⏰ Следующая работа через: {format_time(WORK_COOLDOWN)}"
    )
    
    await message.answer(work_text, parse_mode=ParseMode.HTML)
    logger.info(f"Игрок {player.first_name} (ID: {user_id}) заработал {reward} монет")


@router.message(Command("daily"))
async def cmd_daily(message: Message):
    """Команда /daily - ежедневная награда"""
    user_id = message.from_user.id
    player = await get_player(user_id)
    
    if not player:
        await message.answer("❌ Вы не зарегистрированы! Используйте /start")
        return
    
    # Проверка кулдауна
    can_claim, remaining = check_cooldown(player.last_daily, DAILY_COOLDOWN)
    
    if not can_claim:
        await message.answer(
            f"🎁 <b>Вы уже получили ежедневную награду!</b>\n\n"
            f"Следующая награда через: {format_time(remaining)}\n\n"
            f"🔥 <b>Текущая серия:</b> {player.daily_streak} дней",
            parse_mode=ParseMode.HTML
        )
        return
    
    # Проверка серии (если прошло больше 48 часов, серия сбрасывается)
    if player.last_daily:
        time_since_last = (datetime.utcnow() - player.last_daily).total_seconds()
        if time_since_last > 172800:  # 48 часов
            player.daily_streak = 0
    
    # Увеличиваем серию
    player.daily_streak += 1
    
    # Расчёт награды
    base_reward = DAILY_REWARD
    streak_bonus = (player.daily_streak - 1) * DAILY_STREAK_BONUS
    total_reward = base_reward + streak_bonus
    
    player.coins += total_reward
    player.total_coins_earned += total_reward
    player.last_daily = datetime.utcnow()
    
    await update_player(player)
    
    daily_text = (
        f"🎁 <b>ЕЖЕДНЕВНАЯ НАГРАДА ПОЛУЧЕНА!</b>\n\n"
        f"💰 <b>Базовая награда:</b> {base_reward:,} NC\n"
        f"🔥 <b>Бонус за серию ({player.daily_streak} дней):</b> +{streak_bonus:,} NC\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ <b>ИТОГО:</b> +{total_reward:,} Next Coins\n\n"
        f"💼 <b>Ваш баланс:</b> {player.coins:,} NC\n\n"
        f"💡 <b>Совет:</b> Получайте награду каждый день для увеличения серии!"
    )
    
    await message.answer(daily_text, parse_mode=ParseMode.HTML)
    logger.info(f"Игрок {player.first_name} получил daily: {total_reward} монет (серия: {player.daily_streak})")


@router.message(Command("mine"))
async def cmd_mine(message: Message):
    """Команда /mine - добыча ресурсов"""
    user_id = message.from_user.id
    player = await get_player(user_id)
    
    if not player:
        await message.answer("❌ Вы не зарегистрированы! Используйте /start")
        return
    
    # Проверка кулдауна
    can_mine, remaining = check_cooldown(player.last_mine, MINE_COOLDOWN)
    
    if not can_mine:
        await message.answer(
            f"⛏️ <b>Вы уже добывали ресурсы!</b>\n\n"
            f"Следующая добыча через: {format_time(remaining)}",
            parse_mode=ParseMode.HTML
        )
        return
    
    # Награда
    base_reward = random.randint(MINE_REWARD_MIN, MINE_REWARD_MAX)
    
    # Шанс найти кристаллы (5%)
    found_crystals = 0
    if random.random() < 0.05:
        found_crystals = random.randint(1, 3)
        player.crystals += found_crystals
    
    # Шанс найти осколки силы (10%)
    found_shards = 0
    if random.random() < 0.10:
        found_shards = random.randint(1, 5)
        player.power_shards += found_shards
    
    player.coins += base_reward
    player.total_coins_earned += base_reward
    player.last_mine = datetime.utcnow()
    
    await update_player(player)
    
    mine_text = (
        f"⛏️ <b>ВЫ ДОБЫЛИ РЕСУРСЫ!</b>\n\n"
        f"💰 <b>Монеты:</b> +{base_reward:,} NC\n"
    )
    
    if found_crystals:
        mine_text += f"💎 <b>Кристаллы:</b> +{found_crystals} (редкая находка!)\n"
    
    if found_shards:
        mine_text += f"🔥 <b>Осколки Силы:</b> +{found_shards}\n"
    
    mine_text += (
        f"\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💼 <b>Баланс:</b> {player.coins:,} NC\n"
        f"💎 <b>Кристаллы:</b> {player.crystals}\n"
        f"🔥 <b>Осколки:</b> {player.power_shards}\n\n"
        f"⏰ Следующая добыча через: {format_time(MINE_COOLDOWN)}"
    )
    
    await message.answer(mine_text, parse_mode=ParseMode.HTML)
    logger.info(f"Игрок {player.first_name} добыл: {base_reward} монет, {found_crystals} кристаллов, {found_shards} осколков")


@router.message(Command("balance"))
async def cmd_balance(message: Message):
    """Команда /balance - проверка баланса"""
    user_id = message.from_user.id
    player = await get_player(user_id)
    
    if not player:
        await message.answer("❌ Вы не зарегистрированы! Используйте /start")
        return
    
    balance_text = (
        f"💼 <b>ВАШ БАЛАНС</b>\n\n"
        f"⭐ <b>Next Coins:</b> {player.coins:,}\n"
        f"💎 <b>Кристаллы:</b> {player.crystals}\n"
        f"🔥 <b>Осколки Силы:</b> {player.power_shards}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 <b>Всего заработано:</b> {player.total_coins_earned:,} NC\n\n"
        f"<i>Используйте /work, /daily, /mine для заработка!</i>"
    )
    
    await message.answer(balance_text, parse_mode=ParseMode.HTML)


@router.callback_query(F.data == "economy:work")
async def callback_work(callback: CallbackQuery):
    """Кнопка работы"""
    await callback.message.delete()
    await cmd_work(callback.message)
    await callback.answer()


@router.callback_query(F.data == "economy:daily")
async def callback_daily(callback: CallbackQuery):
    """Кнопка ежедневной награды"""
    await callback.message.delete()
    await cmd_daily(callback.message)
    await callback.answer()


@router.callback_query(F.data == "economy:mine")
async def callback_mine(callback: CallbackQuery):
    """Кнопка добычи"""
    await callback.message.delete()
    await cmd_mine(callback.message)
    await callback.answer()