"""
Обработчик администраторских команд
"""

import logging
from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
from sqlalchemy import select, func

from database.database import async_session, get_player, update_player
from database.models import Player, Guild, ActiveEvent
from config import ADMIN_IDS

router = Router()
logger = logging.getLogger(__name__)


def is_admin(user_id: int) -> bool:
    """Проверка является ли пользователь админом"""
    return user_id in ADMIN_IDS


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    """Команда /admin - меню администратора"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора!")
        return
    
    admin_menu = (
        "👑 <b>ПАНЕЛЬ АДМИНИСТРАТОРА</b>\n\n"
        "<b>📊 СТАТИСТИКА:</b>\n"
        "/stats - Общая статистика бота\n"
        "/top - Топ игроков\n\n"
        "<b>👤 УПРАВЛЕНИЕ ИГРОКАМИ:</b>\n"
        "/give_coins <@user> <кол-во> - Выдать монеты\n"
        "/give_crystals <@user> <кол-во> - Выдать кристаллы\n"
        "/set_level <@user> <уровень> - Установить уровень\n"
        "/ban <@user> - Забанить игрока\n"
        "/unban <@user> - Разбанить игрока\n\n"
        "<b>🎲 СОБЫТИЯ:</b>\n"
        "/spawn_event <тип> - Запустить событие\n"
        "/stop_event <ID> - Остановить событие\n\n"
        "<b>🔧 СИСТЕМА:</b>\n"
        "/broadcast <текст> - Рассылка сообщения\n"
        "/reset_cooldowns <@user> - Сбросить кулдауны\n"
        "/backup - Создать бэкап БД"
    )
    
    await message.answer(admin_menu, parse_mode=ParseMode.HTML)


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    """Команда /stats - статистика бота"""
    if not is_admin(message.from_user.id):
        return
    
    async with async_session() as session:
        # Общее количество игроков
        total_players_result = await session.execute(select(func.count(Player.id)))
        total_players = total_players_result.scalar()
        
        # Активные сегодня (последние 24 часа)
        from datetime import timedelta
        yesterday = datetime.utcnow() - timedelta(days=1)
        active_today_result = await session.execute(
            select(func.count(Player.id)).where(Player.last_active > yesterday)
        )
        active_today = active_today_result.scalar()
        
        # Общая экономика
        total_coins_result = await session.execute(select(func.sum(Player.coins)))
        total_coins = total_coins_result.scalar() or 0
        
        total_crystals_result = await session.execute(select(func.sum(Player.crystals)))
        total_crystals = total_crystals_result.scalar() or 0
        
        # Гильдии
        total_guilds_result = await session.execute(select(func.count(Guild.id)))
        total_guilds = total_guilds_result.scalar()
        
        # Средний уровень
        avg_level_result = await session.execute(select(func.avg(Player.level)))
        avg_level = avg_level_result.scalar() or 0
        
        # Активные события
        active_events_result = await session.execute(
            select(func.count(ActiveEvent.id)).where(ActiveEvent.is_active == True)
        )
        active_events = active_events_result.scalar()
    
    stats_text = (
        f"📊 <b>СТАТИСТИКА БОТА</b>\n\n"
        f"👥 <b>ИГРОКИ:</b>\n"
        f"└ Всего: {total_players:,}\n"
        f"└ Активных за 24ч: {active_today:,}\n"
        f"└ Средний уровень: {avg_level:.1f}\n\n"
        f"💰 <b>ЭКОНОМИКА:</b>\n"
        f"└ Монет в обороте: {total_coins:,}\n"
        f"└ Кристаллов в обороте: {total_crystals:,}\n\n"
        f"🏰 <b>ГИЛЬДИИ:</b>\n"
        f"└ Всего гильдий: {total_guilds}\n\n"
        f"🎲 <b>СОБЫТИЯ:</b>\n"
        f"└ Активных: {active_events}\n\n"
        f"📅 Время сервера: {datetime.utcnow().strftime('%d.%m.%Y %H:%M UTC')}"
    )
    
    await message.answer(stats_text, parse_mode=ParseMode.HTML)
    logger.info(f"Админ {message.from_user.first_name} запросил статистику")


@router.message(Command("give_coins"))
async def cmd_give_coins(message: Message):
    """Команда выдачи монет"""
    if not is_admin(message.from_user.id):
        return
    
    # Парсим аргументы
    args = message.text.split()
    if len(args) < 3:
        await message.answer(
            "Использование: /give_coins @username <количество>\n"
            "или ответьте на сообщение игрока"
        )
        return
    
    try:
        amount = int(args[2])
    except ValueError:
        await message.answer("❌ Укажите корректное количество!")
        return
    
    # Получаем ID игрока
    if message.reply_to_message:
        target_id = message.reply_to_message.from_user.id
    else:
        # TODO: парсинг @username
        await message.answer("❌ Ответьте на сообщение игрока")
        return
    
    player = await get_player(target_id)
    if not player:
        await message.answer("❌ Игрок не зарегистрирован!")
        return
    
    player.coins += amount
    player.total_coins_earned += max(0, amount)
    await update_player(player)
    
    await message.answer(
        f"✅ Выдано {amount:,} монет игроку {player.first_name}",
        parse_mode=ParseMode.HTML
    )
    logger.info(f"Админ выдал {amount} монет игроку {player.first_name}")


@router.message(Command("give_crystals"))
async def cmd_give_crystals(message: Message):
    """Команда выдачи кристаллов"""
    if not is_admin(message.from_user.id):
        return
    
    args = message.text.split()
    if len(args) < 3:
        await message.answer(
            "Использование: /give_crystals @username <количество>\n"
            "или ответьте на сообщение игрока"
        )
        return
    
    try:
        amount = int(args[2])
    except ValueError:
        await message.answer("❌ Укажите корректное количество!")
        return
    
    if message.reply_to_message:
        target_id = message.reply_to_message.from_user.id
    else:
        await message.answer("❌ Ответьте на сообщение игрока")
        return
    
    player = await get_player(target_id)
    if not player:
        await message.answer("❌ Игрок не зарегистрирован!")
        return
    
    player.crystals += amount
    await update_player(player)
    
    await message.answer(
        f"✅ Выдано {amount:,} кристаллов игроку {player.first_name}",
        parse_mode=ParseMode.HTML
    )
    logger.info(f"Админ выдал {amount} кристаллов игроку {player.first_name}")


@router.message(Command("set_level"))
async def cmd_set_level(message: Message):
    """Команда установки уровня"""
    if not is_admin(message.from_user.id):
        return
    
    args = message.text.split()
    if len(args) < 3:
        await message.answer(
            "Использование: /set_level @username <уровень>\n"
            "или ответьте на сообщение игрока"
        )
        return
    
    try:
        level = int(args[2])
    except ValueError:
        await message.answer("❌ Укажите корректный уровень!")
        return
    
    if level < 1 or level > 100:
        await message.answer("❌ Уровень должен быть от 1 до 100!")
        return
    
    if message.reply_to_message:
        target_id = message.reply_to_message.from_user.id
    else:
        await message.answer("❌ Ответьте на сообщение игрока")
        return
    
    player = await get_player(target_id)
    if not player:
        await message.answer("❌ Игрок не зарегистрирован!")
        return
    
    old_level = player.level
    player.level = level
    player.exp = 0
    player.exp_needed = level * 100
    
    # Пересчитываем характеристики
    level_diff = level - old_level
    if level_diff > 0:
        player.max_hp += level_diff * 10
        player.hp = player.max_hp
        player.max_energy += level_diff * 5
        player.energy = player.max_energy
        player.strength += level_diff * 2
        player.agility += level_diff * 2
        player.intelligence += level_diff * 2
        player.defense += level_diff
    
    await update_player(player)
    
    await message.answer(
        f"✅ Уровень игрока {player.first_name} установлен на {level}",
        parse_mode=ParseMode.HTML
    )
    logger.info(f"Админ установил уровень {level} игроку {player.first_name}")


@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message):
    """Команда рассылки сообщений"""
    if not is_admin(message.from_user.id):
        return
    
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer(
            "Использование: /broadcast <текст сообщения>\n\n"
            "Сообщение будет отправлено всем игрокам!"
        )
        return
    
    broadcast_text = args[1]
    
    async with async_session() as session:
        result = await session.execute(select(Player))
        all_players = result.scalars().all()
    
    sent = 0
    failed = 0
    
    status_msg = await message.answer(f"📤 Отправка рассылки для {len(all_players)} игроков...")
    
    for player in all_players:
        try:
            await message.bot.send_message(
                player.telegram_id,
                f"📢 <b>ОБЪЯВЛЕНИЕ ОТ АДМИНИСТРАЦИИ</b>\n\n{broadcast_text}",
                parse_mode=ParseMode.HTML
            )
            sent += 1
        except Exception as e:
            failed += 1
            logger.error(f"Не удалось отправить сообщение игроку {player.telegram_id}: {e}")
    
    await status_msg.edit_text(
        f"✅ <b>Рассылка завершена!</b>\n\n"
        f"✉️ Отправлено: {sent}\n"
        f"❌ Не доставлено: {failed}",
        parse_mode=ParseMode.HTML
    )
    
    logger.info(f"Админ выполнил рассылку: отправлено {sent}, не доставлено {failed}")


@router.message(Command("spawn_event"))
async def cmd_spawn_event(message: Message):
    """Команда запуска события"""
    if not is_admin(message.from_user.id):
        return
    
    args = message.text.split()
    if len(args) < 2:
        await message.answer(
            "Использование: /spawn_event <тип>\n\n"
            "Доступные типы:\n"
            "• meteor_shower - Метеоритный дождь\n"
            "• lucky_merchant - Удачливый торговец\n"
            "• happy_hour - Счастливый час\n"
            "• boss_raid - Нашествие боссов"
        )
        return
    
    event_type = args[1]
    
    from handlers.events import (
        spawn_meteor_shower, 
        spawn_lucky_merchant, 
        spawn_happy_hour, 
        spawn_boss_raid
    )
    
    event_spawners = {
        "meteor_shower": spawn_meteor_shower,
        "lucky_merchant": spawn_lucky_merchant,
        "happy_hour": spawn_happy_hour,
        "boss_raid": spawn_boss_raid
    }
    
    if event_type not in event_spawners:
        await message.answer("❌ Неверный тип события!")
        return
    
    # Запускаем событие
    chat_id = message.chat.id
    await event_spawners[event_type](message.bot, chat_id)
    
    await message.answer(f"✅ Событие '{event_type}' запущено!")
    logger.info(f"Админ запустил событие '{event_type}'")


@router.message(Command("reset_cooldowns"))
async def cmd_reset_cooldowns(message: Message):
    """Команда сброса кулдаунов"""
    if not is_admin(message.from_user.id):
        return
    
    if not message.reply_to_message:
        await message.answer("❌ Ответьте на сообщение игрока")
        return
    
    target_id = message.reply_to_message.from_user.id
    player = await get_player(target_id)
    
    if not player:
        await message.answer("❌ Игрок не зарегистрирован!")
        return
    
    # Сбрасываем все кулдауны
    player.last_work = None
    player.last_daily = None
    player.last_hunt = None
    player.last_pvp = None
    player.last_mine = None
    
    # Восстанавливаем энергию
    player.energy = player.max_energy
    player.hp = player.max_hp
    
    await update_player(player)
    
    await message.answer(
        f"✅ Кулдауны игрока {player.first_name} сброшены!\n"
        f"Энергия и HP восстановлены.",
        parse_mode=ParseMode.HTML
    )
    logger.info(f"Админ сбросил кулдауны игрока {player.first_name}")


@router.message(Command("top"))
async def cmd_top(message: Message):
    """Команда топ игроков"""
    async with async_session() as session:
        # Топ по уровню
        top_level_result = await session.execute(
            select(Player)
            .order_by(Player.level.desc(), Player.exp.desc())
            .limit(10)
        )
        top_level = top_level_result.scalars().all()
        
        # Топ по монетам
        top_coins_result = await session.execute(
            select(Player)
            .order_by(Player.total_coins_earned.desc())
            .limit(10)
        )
        top_coins = top_coins_result.scalars().all()
    
    # Формируем топ по уровню
    level_text = "🏆 <b>ТОП 10 ПО УРОВНЮ</b>\n\n"
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    
    for idx, player in enumerate(top_level):
        level_text += (
            f"{medals[idx]} <b>{player.first_name}</b>\n"
            f"   └ Уровень {player.level} | {player.exp}/{player.exp_needed} опыта\n"
        )
    
    # Формируем топ по монетам
    coins_text = "\n💰 <b>ТОП 10 ПО МОНЕТАМ</b>\n\n"
    
    for idx, player in enumerate(top_coins):
        coins_text += (
            f"{medals[idx]} <b>{player.first_name}</b>\n"
            f"   └ {player.total_coins_earned:,} монет заработано\n"
        )
    
    await message.answer(level_text + coins_text, parse_mode=ParseMode.HTML)