"""
Обработчик случайных событий
"""

import logging
import random
from datetime import datetime, timedelta
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.enums import ParseMode

from database.database import async_session, get_player, update_player
from database.models import ActiveEvent
from keyboards import get_back_button
from config import RANDOM_EVENTS

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("events"))
async def cmd_events(message: Message):
    """Команда /events - показать активные события"""
    async with async_session() as session:
        from sqlalchemy import select
        result = await session.execute(
            select(ActiveEvent).where(ActiveEvent.is_active == True)
        )
        active_events = result.scalars().all()
    
    if not active_events:
        await message.answer(
            "📭 <b>Нет активных событий</b>\n\n"
            "События появляются случайным образом каждые 2-4 часа!\n"
            "Следите за уведомлениями в чате.",
            parse_mode=ParseMode.HTML
        )
        return
    
    events_text = "🎲 <b>АКТИВНЫЕ СОБЫТИЯ</b>\n\n"
    
    for event in active_events:
        event_data = RANDOM_EVENTS.get(event.event_type, {})
        time_left = (event.ends_at - datetime.utcnow()).total_seconds()
        
        if time_left > 0:
            minutes = int(time_left // 60)
            events_text += (
                f"{event_data.get('name', 'Событие')}\n"
                f"├ {event_data.get('description', '')}\n"
                f"└ ⏰ Осталось: {minutes} минут\n\n"
            )
    
    await message.answer(events_text, parse_mode=ParseMode.HTML)


async def spawn_meteor_shower(bot, chat_id: int):
    """Событие: Метеоритный дождь"""
    event_data = RANDOM_EVENTS["meteor_shower"]
    
    # Создаём событие в БД
    async with async_session() as session:
        event = ActiveEvent(
            event_type="meteor_shower",
            started_at=datetime.utcnow(),
            ends_at=datetime.utcnow() + timedelta(seconds=event_data["duration"]),
            data="{}",
            participants="[]",
            is_active=True
        )
        session.add(event)
        await session.commit()
        event_id = event.id
    
    announcement = (
        f"🌟 <b>МЕТЕОРИТНЫЙ ДОЖДЬ!</b> 🌟\n\n"
        f"С неба падают метеориты с сокровищами!\n\n"
        f"🎁 <b>Награды:</b>\n"
        f"└ 💰 {event_data['reward_coins']:,} монет\n"
        f"└ ✨ {event_data['reward_exp']} опыта\n\n"
        f"👥 Первые {event_data['max_participants']} участников получат награду!\n\n"
        f"Напишите /catch чтобы поймать метеорит!"
    )
    
    await bot.send_message(chat_id, announcement, parse_mode=ParseMode.HTML)
    logger.info("Событие: Метеоритный дождь начался")


async def spawn_lucky_merchant(bot, chat_id: int):
    """Событие: Удачливый торговец"""
    event_data = RANDOM_EVENTS["lucky_merchant"]
    
    async with async_session() as session:
        event = ActiveEvent(
            event_type="lucky_merchant",
            started_at=datetime.utcnow(),
            ends_at=datetime.utcnow() + timedelta(seconds=event_data["duration"]),
            data=f'{{"discount": {event_data["discount"]}}}',
            is_active=True
        )
        session.add(event)
        await session.commit()
    
    announcement = (
        f"🎁 <b>УДАЧЛИВЫЙ ТОРГОВЕЦ!</b>\n\n"
        f"В Некстграде появился странствующий торговец со скидками!\n\n"
        f"💰 Скидка на ВСЕ товары: {int(event_data['discount'] * 100)}%\n"
        f"⏰ Продлится: {event_data['duration'] // 60} минут\n\n"
        f"Используйте /shop чтобы купить по выгодной цене!"
    )
    
    await bot.send_message(chat_id, announcement, parse_mode=ParseMode.HTML)
    logger.info("Событие: Удачливый торговец появился")


async def spawn_happy_hour(bot, chat_id: int):
    """Событие: Счастливый час"""
    event_data = RANDOM_EVENTS["happy_hour"]
    
    async with async_session() as session:
        event = ActiveEvent(
            event_type="happy_hour",
            started_at=datetime.utcnow(),
            ends_at=datetime.utcnow() + timedelta(seconds=event_data["duration"]),
            data=f'{{"multiplier": {event_data["multiplier"]}}}',
            is_active=True
        )
        session.add(event)
        await session.commit()
    
    announcement = (
        f"⚡ <b>СЧАСТЛИВЫЙ ЧАС!</b> ⚡\n\n"
        f"Все награды УДВОЕНЫ на следующий час!\n\n"
        f"✨ Множитель: x{event_data['multiplier']}\n"
        f"⏰ Продлится: {event_data['duration'] // 3600} час\n\n"
        f"Самое время заработать! 💰\n"
        f"Используйте /work, /mine, /hunt для максимальной выгоды!"
    )
    
    await bot.send_message(chat_id, announcement, parse_mode=ParseMode.HTML)
    logger.info("Событие: Счастливый час начался")


async def spawn_boss_raid(bot, chat_id: int):
    """Событие: Нашествие боссов"""
    event_data = RANDOM_EVENTS["boss_raid"]
    
    async with async_session() as session:
        event = ActiveEvent(
            event_type="boss_raid",
            started_at=datetime.utcnow(),
            ends_at=datetime.utcnow() + timedelta(seconds=event_data["duration"]),
            data=f'{{"boss_hp": {event_data["boss_hp"]}, "boss_damage": {event_data["boss_damage"]}}}',
            participants="[]",
            is_active=True
        )
        session.add(event)
        await session.commit()
    
    announcement = (
        f"💀 <b>НАШЕСТВИЕ БОССОВ!</b> 💀\n\n"
        f"Мощный босс атакует Некстград!\n\n"
        f"🐉 <b>Характеристики:</b>\n"
        f"└ ❤️ HP: {event_data['boss_hp']}\n"
        f"└ ⚔️ Урон: {event_data['boss_damage']}\n\n"
        f"🎁 <b>Награды за победу:</b>\n"
        f"└ 💰 {event_data['reward_coins']:,} монет\n"
        f"└ ✨ {event_data['reward_exp']} опыта\n\n"
        f"👥 Объединитесь для победы!\n"
        f"⏰ Время: {event_data['duration'] // 60} минут\n\n"
        f"Используйте /boss_attack чтобы атаковать!"
    )
    
    await bot.send_message(chat_id, announcement, parse_mode=ParseMode.HTML)
    logger.info("Событие: Нашествие боссов началось")


@router.message(Command("catch"))
async def cmd_catch_meteor(message: Message):
    """Команда поймать метеорит"""
    user_id = message.from_user.id
    player = await get_player(user_id)
    
    if not player:
        await message.answer("❌ Вы не зарегистрированы! Используйте /start")
        return
    
    # Проверяем активное событие
    async with async_session() as session:
        from sqlalchemy import select
        result = await session.execute(
            select(ActiveEvent).where(
                ActiveEvent.event_type == "meteor_shower",
                ActiveEvent.is_active == True
            )
        )
        event = result.scalar_one_or_none()
        
        if not event:
            await message.answer("❌ Сейчас нет метеоритного дождя!")
            return
        
        # Проверяем, не участвовал ли уже
        import json
        participants = json.loads(event.participants or "[]")
        
        if user_id in participants:
            await message.answer("❌ Вы уже поймали метеорит!")
            return
        
        event_data = RANDOM_EVENTS["meteor_shower"]
        
        if len(participants) >= event_data["max_participants"]:
            await message.answer("❌ Все метеориты уже пойманы!")
            return
        
        # Добавляем участника
        participants.append(user_id)
        event.participants = json.dumps(participants)
        session.add(event)
        
        # Выдаём награды
        player.coins += event_data["reward_coins"]
        player.total_coins_earned += event_data["reward_coins"]
        player.exp += event_data["reward_exp"]
        
        await session.commit()
    
    await update_player(player)
    
    result_text = (
        f"🌟 <b>ВЫ ПОЙМАЛИ МЕТЕОРИТ!</b>\n\n"
        f"🎁 <b>Награды:</b>\n"
        f"└ 💰 +{event_data['reward_coins']:,} монет\n"
        f"└ ✨ +{event_data['reward_exp']} опыта\n\n"
        f"👥 Участников: {len(participants)}/{event_data['max_participants']}"
    )
    
    await message.answer(result_text, parse_mode=ParseMode.HTML)
    logger.info(f"Игрок {player.first_name} поймал метеорит")


@router.message(Command("boss_attack"))
async def cmd_boss_attack(message: Message):
    """Команда атаковать босса"""
    user_id = message.from_user.id
    player = await get_player(user_id)
    
    if not player:
        await message.answer("❌ Вы не зарегистрированы! Используйте /start")
        return
    
    # Проверяем активное событие
    async with async_session() as session:
        from sqlalchemy import select
        result = await session.execute(
            select(ActiveEvent).where(
                ActiveEvent.event_type == "boss_raid",
                ActiveEvent.is_active == True
            )
        )
        event = result.scalar_one_or_none()
        
        if not event:
            await message.answer("❌ Сейчас нет нашествия боссов!")
            return
        
        # Проверяем энергию
        if player.energy < 30:
            await message.answer("⚡ Недостаточно энергии! Нужно 30")
            return
        
        import json
        event_data_dict = json.loads(event.data)
        boss_hp = event_data_dict.get("boss_hp", 5000)
        
        # Наносим урон
        from utils.calculations import calculate_damage
        damage = calculate_damage(player.strength, player.agility, player.intelligence)
        damage = random.randint(int(damage * 0.8), int(damage * 1.2))
        
        boss_hp -= damage
        event_data_dict["boss_hp"] = max(0, boss_hp)
        event.data = json.dumps(event_data_dict)
        
        # Добавляем в участники
        participants = json.loads(event.participants or "[]")
        if user_id not in participants:
            participants.append(user_id)
            event.participants = json.dumps(participants)
        
        player.energy -= 30
        
        if boss_hp <= 0:
            # БОСС ПОБЕЖДЁН!
            event.is_active = False
            
            # Награды всем участникам
            reward_data = RANDOM_EVENTS["boss_raid"]
            coins_per_player = reward_data["reward_coins"] // len(participants)
            exp_per_player = reward_data["reward_exp"] // len(participants)
            
            player.coins += coins_per_player
            player.total_coins_earned += coins_per_player
            player.exp += exp_per_player
            
            await update_player(player)
            
            session.add(event)
            await session.commit()
            
            victory_text = (
                f"🏆 <b>БОСС ПОВЕРЖЕН!</b>\n\n"
                f"⚔️ Вы нанесли финальный удар: {damage} урона!\n\n"
                f"🎁 <b>Ваши награды:</b>\n"
                f"└ 💰 {coins_per_player:,} монет\n"
                f"└ ✨ {exp_per_player} опыта\n\n"
                f"👥 Участвовало игроков: {len(participants)}"
            )
            
            await message.answer(victory_text, parse_mode=ParseMode.HTML)
            
            # Уведомление в чат
            from aiogram import Bot
            bot = message.bot
            await bot.send_message(
                message.chat.id,
                f"🎉 <b>БОСС ПОБЕЖДЁН!</b>\n\n"
                f"Герои Некстграда одержали победу!\n"
                f"Спасибо всем {len(participants)} участникам!",
                parse_mode=ParseMode.HTML
            )
        else:
            session.add(event)
            await session.commit()
            await update_player(player)
            
            attack_text = (
                f"⚔️ <b>ВЫ АТАКОВАЛИ БОССА!</b>\n\n"
                f"💥 Нанесено урона: {damage}\n"
                f"❤️ Осталось HP: {boss_hp:,}\n\n"
                f"⚡ -30 энергии\n"
                f"👥 Участников: {len(participants)}"
            )
            
            await message.answer(attack_text, parse_mode=ParseMode.HTML)


async def cleanup_expired_events():
    """Очистка истёкших событий"""
    async with async_session() as session:
        from sqlalchemy import select
        result = await session.execute(
            select(ActiveEvent).where(
                ActiveEvent.is_active == True,
                ActiveEvent.ends_at < datetime.utcnow()
            )
        )
        expired_events = result.scalars().all()
        
        for event in expired_events:
            event.is_active = False
            session.add(event)
        
        await session.commit()
        
        if expired_events:
            logger.info(f"Очищено {len(expired_events)} истёкших событий")