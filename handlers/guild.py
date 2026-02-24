"""
Обработчик гильдий
"""

import logging
from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.enums import ParseMode
from sqlalchemy import select, func

from database.database import get_player, update_player, async_session
from database.models import Guild
from keyboards import get_guild_menu, get_confirm_keyboard, get_back_button
from config import GUILD_CREATE_COST, GUILD_MAX_MEMBERS

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("guild"))
async def cmd_guild(message: Message):
    """Команда /guild - меню гильдии"""
    user_id = message.from_user.id
    player = await get_player(user_id)
    
    if not player:
        await message.answer("❌ Вы не зарегистрированы! Используйте /start")
        return
    
    has_guild = player.guild_id is not None
    
    await message.answer(
        "🏰 <b>МЕНЮ ГИЛЬДИИ</b>\n\n"
        "Выберите действие:",
        reply_markup=get_guild_menu(has_guild),
        parse_mode=ParseMode.HTML
    )


@router.message(Command("guild_create"))
async def cmd_guild_create(message: Message):
    """Команда создания гильдии"""
    user_id = message.from_user.id
    player = await get_player(user_id)
    
    if not player:
        await message.answer("❌ Вы не зарегистрированы! Используйте /start")
        return
    
    if player.guild_id:
        await message.answer("❌ Вы уже состоите в гильдии!")
        return
    
    if player.coins < GUILD_CREATE_COST:
        await message.answer(
            f"💰 <b>Недостаточно средств!</b>\n\n"
            f"Стоимость создания гильдии: {GUILD_CREATE_COST:,} монет\n"
            f"У вас: {player.coins:,} монет",
            parse_mode=ParseMode.HTML
        )
        return
    
    # Получаем название из текста команды
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer(
            "📝 <b>СОЗДАНИЕ ГИЛЬДИИ</b>\n\n"
            f"💰 Стоимость: {GUILD_CREATE_COST:,} монет\n\n"
            "Использование:\n"
            "/guild_create Название Гильдии\n\n"
            "Требования:\n"
            "• От 3 до 30 символов\n"
            "• Только буквы и пробелы",
            parse_mode=ParseMode.HTML
        )
        return
    
    guild_name = args[1].strip()
    
    # Валидация названия
    if len(guild_name) < 3 or len(guild_name) > 30:
        await message.answer("❌ Название должно быть от 3 до 30 символов!")
        return
    
    # Проверка уникальности
    async with async_session() as session:
        result = await session.execute(
            select(Guild).where(func.lower(Guild.name) == guild_name.lower())
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            await message.answer("❌ Гильдия с таким названием уже существует!")
            return
        
        # Создаём гильдию
        guild = Guild(
            name=guild_name,
            leader_id=user_id,
            treasury=0,
            level=1,
            exp=0,
            total_members=1,
            created_at=datetime.utcnow()
        )
        session.add(guild)
        await session.commit()
        await session.refresh(guild)
        
        # Обновляем игрока
        player.guild_id = guild.id
        player.guild_role = "leader"
        player.coins -= GUILD_CREATE_COST
        await update_player(player)
    
    creation_text = (
        f"🏰 <b>ГИЛЬДИЯ СОЗДАНА!</b>\n\n"
        f"📛 <b>Название:</b> {guild_name}\n"
        f"👑 <b>Лидер:</b> {player.first_name}\n"
        f"📊 <b>Уровень:</b> 1\n"
        f"👥 <b>Участников:</b> 1/{GUILD_MAX_MEMBERS}\n\n"
        f"💰 Списано {GUILD_CREATE_COST:,} монет\n\n"
        f"Используйте /guild для управления гильдией!"
    )
    
    await message.answer(creation_text, parse_mode=ParseMode.HTML)
    logger.info(f"Создана гильдия '{guild_name}' лидером {player.first_name}")


@router.message(Command("guild_info"))
async def cmd_guild_info(message: Message):
    """Информация о гильдии"""
    user_id = message.from_user.id
    player = await get_player(user_id)
    
    if not player:
        await message.answer("❌ Вы не зарегистрированы! Используйте /start")
        return
    
    if not player.guild_id:
        await message.answer("❌ Вы не состоите в гильдии!")
        return
    
    async with async_session() as session:
        result = await session.execute(
            select(Guild).where(Guild.id == player.guild_id)
        )
        guild = result.scalar_one_or_none()
        
        if not guild:
            await message.answer("❌ Гильдия не найдена!")
            return
        
        # Получаем информацию о лидере
        leader_result = await session.execute(
            select(player.__class__).where(player.__class__.id == guild.leader_id)
        )
        leader = leader_result.scalar_one_or_none()
        leader_name = leader.first_name if leader else "Неизвестен"
    
    role_emoji = {
        "leader": "👑",
        "officer": "⭐",
        "member": "👤"
    }
    
    info_text = (
        f"🏰 <b>ИНФОРМАЦИЯ О ГИЛЬДИИ</b>\n\n"
        f"📛 <b>Название:</b> {guild.name}\n"
        f"👑 <b>Лидер:</b> {leader_name}\n"
        f"📊 <b>Уровень:</b> {guild.level}\n"
        f"✨ <b>Опыт:</b> {guild.exp}\n\n"
        f"👥 <b>Участники:</b> {guild.total_members}/{GUILD_MAX_MEMBERS}\n"
        f"💰 <b>Казна:</b> {guild.treasury:,} монет\n\n"
        f"🏆 <b>СТАТИСТИКА:</b>\n"
        f"└ Побед в войнах: {guild.wars_won}\n"
        f"└ Поражений: {guild.wars_lost}\n\n"
        f"{role_emoji.get(player.guild_role, '👤')} <b>Ваша роль:</b> {player.guild_role}\n\n"
        f"📅 Создана: {guild.created_at.strftime('%d.%m.%Y')}"
    )
    
    await message.answer(info_text, parse_mode=ParseMode.HTML)


@router.message(Command("guild_leave"))
async def cmd_guild_leave(message: Message):
    """Покинуть гильдию"""
    user_id = message.from_user.id
    player = await get_player(user_id)
    
    if not player:
        await message.answer("❌ Вы не зарегистрированы! Используйте /start")
        return
    
    if not player.guild_id:
        await message.answer("❌ Вы не состоите в гильдии!")
        return
    
    if player.guild_role == "leader":
        await message.answer(
            "❌ <b>Лидер не может покинуть гильдию!</b>\n\n"
            "Сначала передайте лидерство другому участнику "
            "или распустите гильдию.",
            parse_mode=ParseMode.HTML
        )
        return
    
    async with async_session() as session:
        # Получаем гильдию
        result = await session.execute(
            select(Guild).where(Guild.id == player.guild_id)
        )
        guild = result.scalar_one_or_none()
        
        if guild:
            guild.total_members -= 1
            session.add(guild)
        
        # Обновляем игрока
        guild_name = guild.name if guild else "Неизвестна"
        player.guild_id = None
        player.guild_role = "member"
        
        await session.commit()
    
    await update_player(player)
    
    await message.answer(
        f"🚪 <b>Вы покинули гильдию '{guild_name}'</b>\n\n"
        f"Вы можете создать новую гильдию или вступить в существующую!",
        parse_mode=ParseMode.HTML
    )
    
    logger.info(f"Игрок {player.first_name} покинул гильдию '{guild_name}'")


@router.message(Command("guild_donate"))
async def cmd_guild_donate(message: Message):
    """Пожертвовать в казну гильдии"""
    user_id = message.from_user.id
    player = await get_player(user_id)
    
    if not player:
        await message.answer("❌ Вы не зарегистрированы! Используйте /start")
        return
    
    if not player.guild_id:
        await message.answer("❌ Вы не состоите в гильдии!")
        return
    
    # Получаем сумму
    args = message.text.split()
    if len(args) < 2:
        await message.answer(
            "💰 <b>ПОЖЕРТВОВАНИЕ В КАЗНУ</b>\n\n"
            "Использование: /guild_donate <сумма>\n"
            "Пример: /guild_donate 1000",
            parse_mode=ParseMode.HTML
        )
        return
    
    try:
        amount = int(args[1])
    except ValueError:
        await message.answer("❌ Укажите корректную сумму!")
        return
    
    if amount <= 0:
        await message.answer("❌ Сумма должна быть положительной!")
        return
    
    if player.coins < amount:
        await message.answer(
            f"💰 <b>Недостаточно монет!</b>\n\n"
            f"У вас: {player.coins:,}\n"
            f"Нужно: {amount:,}",
            parse_mode=ParseMode.HTML
        )
        return
    
    async with async_session() as session:
        result = await session.execute(
            select(Guild).where(Guild.id == player.guild_id)
        )
        guild = result.scalar_one_or_none()
        
        if not guild:
            await message.answer("❌ Гильдия не найдена!")
            return
        
        # Переводим деньги
        player.coins -= amount
        guild.treasury += amount
        guild.exp += amount // 10  # 1 опыт за каждые 10 монет
        
        session.add(guild)
        await session.commit()
    
    await update_player(player)
    
    await message.answer(
        f"💝 <b>ПОЖЕРТВОВАНИЕ ПРИНЯТО!</b>\n\n"
        f"Вы пожертвовали {amount:,} монет в казну гильдии!\n\n"
        f"💰 Казна гильдии: {guild.treasury:,} монет\n"
        f"✨ Опыт гильдии: +{amount // 10}",
        parse_mode=ParseMode.HTML
    )


@router.callback_query(F.data == "guild:info")
async def callback_guild_info(callback: CallbackQuery):
    """Кнопка информации о гильдии"""
    await callback.message.delete()
    await cmd_guild_info(callback.message)
    await callback.answer()


@router.callback_query(F.data == "guild:leave")
async def callback_guild_leave(callback: CallbackQuery):
    """Кнопка выхода из гильдии"""
    await callback.message.edit_text(
        "⚠️ <b>Вы уверены, что хотите покинуть гильдию?</b>\n\n"
        "Это действие нельзя отменить!",
        reply_markup=get_confirm_keyboard("guild_leave"),
        parse_mode=ParseMode.HTML
    )
    await callback.answer()


@router.callback_query(F.data.startswith("confirm:guild_leave:"))
async def callback_confirm_leave(callback: CallbackQuery):
    """Подтверждение выхода"""
    action = callback.data.split(":")[2]
    
    if action == "yes":
        await callback.message.delete()
        await cmd_guild_leave(callback.message)
    else:
        await callback.message.edit_text(
            "✅ Действие отменено",
            parse_mode=ParseMode.HTML
        )
    
    await callback.answer()