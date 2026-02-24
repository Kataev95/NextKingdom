"""
Обработчик боевой системы
"""

import logging
import random
from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.enums import ParseMode

from database.database import get_player, update_player, async_session
from database.models import BattleLog
from keyboards import get_combat_menu, get_monster_selection, get_back_button
from utils.calculations import calculate_damage, calculate_exp_reward, check_level_up
from config import (
    HUNT_COOLDOWN, HUNT_ENERGY_COST,
    PVP_COOLDOWN, PVP_ENERGY_COST,
    MONSTERS, HERO_CLASSES
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


@router.message(Command("hunt"))
async def cmd_hunt(message: Message):
    """Команда /hunt - охота на монстров"""
    user_id = message.from_user.id
    player = await get_player(user_id)
    
    if not player:
        await message.answer("❌ Вы не зарегистрированы! Используйте /start")
        return
    
    # Проверка кулдауна
    can_hunt, remaining = check_cooldown(player.last_hunt, HUNT_COOLDOWN)
    
    if not can_hunt:
        await message.answer(
            f"⏰ <b>Вы недавно охотились!</b>\n\n"
            f"Следующая охота через: {format_time(remaining)}",
            parse_mode=ParseMode.HTML
        )
        return
    
    # Проверка энергии
    if player.energy < HUNT_ENERGY_COST:
        await message.answer(
            f"⚡ <b>Недостаточно энергии!</b>\n\n"
            f"Необходимо: {HUNT_ENERGY_COST}\n"
            f"У вас: {player.energy}\n\n"
            f"<i>Энергия восстанавливается со временем (1 в минуту)</i>",
            parse_mode=ParseMode.HTML
        )
        return
    
    # Показываем выбор монстров
    await message.answer(
        "🐺 <b>ВЫБЕРИТЕ ЦЕЛЬ ДЛЯ ОХОТЫ:</b>\n\n"
        "Выберите монстра в соответствии с вашим уровнем!",
        reply_markup=get_monster_selection(player.level),
        parse_mode=ParseMode.HTML
    )


@router.callback_query(F.data.startswith("hunt:"))
async def process_hunt(callback: CallbackQuery):
    """Обработка охоты на монстра"""
    monster_id = callback.data.split(":")[1]
    
    if monster_id not in MONSTERS:
        await callback.answer("❌ Неверный монстр!", show_alert=True)
        return
    
    user_id = callback.from_user.id
    player = await get_player(user_id)
    
    if not player:
        await callback.answer("❌ Вы не зарегистрированы!", show_alert=True)
        return
    
    # Проверки
    if player.energy < HUNT_ENERGY_COST:
        await callback.answer(f"⚡ Недостаточно энергии! Нужно {HUNT_ENERGY_COST}", show_alert=True)
        return
    
    monster = MONSTERS[monster_id]
    
    if player.level < monster['level_requirement']:
        await callback.answer(f"❌ Нужен {monster['level_requirement']} уровень!", show_alert=True)
        return
    
    # Характеристики
    player_damage = calculate_damage(player.strength, player.agility, player.intelligence)
    monster_hp = monster['hp']
    monster_damage = monster['damage']
    monster_defense = monster['defense']
    
    # Симуляция боя
    battle_log = []
    current_monster_hp = monster_hp
    current_player_hp = player.hp
    
    round_num = 1
    while current_monster_hp > 0 and current_player_hp > 0:
        # Атака игрока
        player_hit = max(1, player_damage - monster_defense + random.randint(-5, 5))
        current_monster_hp -= player_hit
        battle_log.append(f"⚔️ Раунд {round_num}: Вы нанесли {player_hit} урона")
        
        if current_monster_hp <= 0:
            break
        
        # Атака монстра
        monster_hit = max(1, monster_damage - player.defense + random.randint(-3, 3))
        current_player_hp -= monster_hit
        battle_log.append(f"💥 {monster['name']} нанёс {monster_hit} урона")
        
        round_num += 1
        
        # Максимум 10 раундов
        if round_num > 10:
            break
    
    # Результат боя
    if current_monster_hp <= 0:
        # ПОБЕДА!
        coins_reward = random.randint(*monster['coins_reward'])
        exp_reward = calculate_exp_reward(monster['exp_reward'], player.level)
        
        player.coins += coins_reward
        player.total_coins_earned += coins_reward
        player.exp += exp_reward
        player.total_monsters_killed += 1
        player.energy -= HUNT_ENERGY_COST
        player.hp = current_player_hp
        player.last_hunt = datetime.utcnow()
        
        # Проверка повышения уровня
        level_up_text = ""
        if check_level_up(player):
            level_up_text = f"\n\n🎉 <b>УРОВЕНЬ ПОВЫШЕН!</b> Теперь вы {player.level} уровня!"
        
        await update_player(player)
        
        # Сохраняем лог боя
        async with async_session() as session:
            battle = BattleLog(
                attacker_id=user_id,
                defender_id=None,
                battle_type="pve",
                winner_id=user_id,
                attacker_damage=player_damage * round_num,
                defender_damage=monster_damage * (round_num - 1),
                rewards=f"coins:{coins_reward},exp:{exp_reward}"
            )
            session.add(battle)
            await session.commit()
        
        result_text = (
            f"🏆 <b>ПОБЕДА!</b>\n\n"
            f"Вы победили {monster['emoji']} <b>{monster['name']}</b>!\n\n"
            f"📊 <b>БОЙ:</b>\n"
            f"└ Раундов: {round_num}\n"
            f"└ Нанесено урона: {monster_hp}\n"
            f"└ Получено урона: {player.max_hp - current_player_hp}\n\n"
            f"🎁 <b>НАГРАДЫ:</b>\n"
            f"└ 💰 {coins_reward:,} Next Coins\n"
            f"└ ✨ {exp_reward} опыта\n\n"
            f"📊 <b>СОСТОЯНИЕ:</b>\n"
            f"└ ❤️ HP: {current_player_hp}/{player.max_hp}\n"
            f"└ ⚡ Энергия: {player.energy}/{player.max_energy}\n"
            f"└ 📈 Опыт: {player.exp}/{player.exp_needed}"
            f"{level_up_text}"
        )
        
        await callback.message.edit_text(result_text, parse_mode=ParseMode.HTML)
        await callback.answer("🏆 Победа!", show_alert=False)
        
        logger.info(f"Игрок {player.first_name} победил {monster['name']}")
    
    else:
        # ПОРАЖЕНИЕ
        player.hp = max(1, current_player_hp)
        player.energy -= HUNT_ENERGY_COST
        player.last_hunt = datetime.utcnow()
        
        await update_player(player)
        
        result_text = (
            f"💀 <b>ПОРАЖЕНИЕ...</b>\n\n"
            f"{monster['emoji']} <b>{monster['name']}</b> оказался сильнее!\n\n"
            f"📊 <b>БОЙ:</b>\n"
            f"└ Раундов: {round_num}\n"
            f"└ Осталось HP монстра: {current_monster_hp}\n\n"
            f"💔 <b>ВЫ ПОТЕРЯЛИ:</b>\n"
            f"└ ⚡ {HUNT_ENERGY_COST} энергии\n\n"
            f"💡 <b>Совет:</b> Улучшите снаряжение или повысьте уровень!"
        )
        
        await callback.message.edit_text(result_text, parse_mode=ParseMode.HTML)
        await callback.answer("💀 Поражение...", show_alert=False)


@router.message(Command("pvp"))
async def cmd_pvp(message: Message):
    """Команда /pvp - дуэль с игроком"""
    user_id = message.from_user.id
    player = await get_player(user_id)
    
    if not player:
        await message.answer("❌ Вы не зарегистрированы! Используйте /start")
        return
    
    # Проверка кулдауна
    can_pvp, remaining = check_cooldown(player.last_pvp, PVP_COOLDOWN)
    
    if not can_pvp:
        await message.answer(
            f"⏰ <b>Вы недавно дуэлились!</b>\n\n"
            f"Следующая дуэль через: {format_time(remaining)}",
            parse_mode=ParseMode.HTML
        )
        return
    
    # Проверка энергии
    if player.energy < PVP_ENERGY_COST:
        await message.answer(
            f"⚡ <b>Недостаточно энергии!</b>\n\n"
            f"Необходимо: {PVP_ENERGY_COST}\n"
            f"У вас: {player.energy}",
            parse_mode=ParseMode.HTML
        )
        return
    
    # Проверка упоминания противника
    if not message.reply_to_message:
        await message.answer(
            "⚔️ <b>КАК ВЫЗВАТЬ НА ДУЭЛЬ:</b>\n\n"
            "Ответьте на сообщение игрока командой /pvp\n"
            "или используйте: /pvp @username",
            parse_mode=ParseMode.HTML
        )
        return
    
    opponent_id = message.reply_to_message.from_user.id
    
    if opponent_id == user_id:
        await message.answer("❌ Нельзя драться с самим собой!")
        return
    
    opponent = await get_player(opponent_id)
    
    if not opponent:
        await message.answer("❌ Этот игрок не зарегистрирован!")
        return
    
    # Симуляция PvP боя
    player_power = calculate_damage(player.strength, player.agility, player.intelligence)
    opponent_power = calculate_damage(opponent.strength, opponent.agility, opponent.intelligence)
    
    # Случайность ±20%
    player_power = int(player_power * random.uniform(0.8, 1.2))
    opponent_power = int(opponent_power * random.uniform(0.8, 1.2))
    
    if player_power > opponent_power:
        # ПОБЕДА
        coins_reward = int(opponent.coins * 0.05)  # 5% от монет противника
        exp_reward = opponent.level * 10
        
        player.coins += coins_reward
        player.total_coins_earned += coins_reward
        player.exp += exp_reward
        player.total_pvp_wins += 1
        player.energy -= PVP_ENERGY_COST
        player.last_pvp = datetime.utcnow()
        
        opponent.coins = max(0, opponent.coins - coins_reward)
        opponent.total_pvp_losses += 1
        
        await update_player(player)
        await update_player(opponent)
        
        # Сохраняем лог
        async with async_session() as session:
            battle = BattleLog(
                attacker_id=user_id,
                defender_id=opponent_id,
                battle_type="pvp",
                winner_id=user_id,
                attacker_damage=player_power,
                defender_damage=opponent_power,
                rewards=f"coins:{coins_reward},exp:{exp_reward}"
            )
            session.add(battle)
            await session.commit()
        
        result_text = (
            f"🏆 <b>ПОБЕДА В ДУЭЛИ!</b>\n\n"
            f"⚔️ Вы победили <b>{opponent.first_name}</b>!\n\n"
            f"📊 <b>ХАРАКТЕРИСТИКИ:</b>\n"
            f"└ Ваша сила: {player_power}\n"
            f"└ Сила противника: {opponent_power}\n\n"
            f"🎁 <b>НАГРАДЫ:</b>\n"
            f"└ 💰 {coins_reward:,} монет\n"
            f"└ ✨ {exp_reward} опыта\n\n"
            f"🏅 <b>Побед в PvP:</b> {player.total_pvp_wins}"
        )
        
        await message.answer(result_text, parse_mode=ParseMode.HTML)
        logger.info(f"PvP: {player.first_name} победил {opponent.first_name}")
        
    else:
        # ПОРАЖЕНИЕ
        player.total_pvp_losses += 1
        player.energy -= PVP_ENERGY_COST
        player.last_pvp = datetime.utcnow()
        
        opponent.total_pvp_wins += 1
        
        await update_player(player)
        await update_player(opponent)
        
        result_text = (
            f"💔 <b>ПОРАЖЕНИЕ В ДУЭЛИ</b>\n\n"
            f"⚔️ <b>{opponent.first_name}</b> оказался сильнее!\n\n"
            f"📊 <b>ХАРАКТЕРИСТИКИ:</b>\n"
            f"└ Ваша сила: {player_power}\n"
            f"└ Сила противника: {opponent_power}\n\n"
            f"💡 <b>Совет:</b> Прокачайтесь и попробуйте снова!"
        )
        
        await message.answer(result_text, parse_mode=ParseMode.HTML)


@router.message(Command("raid"))
async def cmd_raid(message: Message):
    """Команда /raid - групповой рейд"""
    await message.answer(
        "👥 <b>ГРУППОВОЙ РЕЙД</b>\n\n"
        "🚧 Эта функция находится в разработке!\n\n"
        "Скоро вы сможете объединяться с другими игроками "
        "для сражений с мощными боссами!\n\n"
        "Следите за обновлениями! 🎮",
        parse_mode=ParseMode.HTML
    )


@router.message(Command("tower"))
async def cmd_tower(message: Message):
    """Команда /tower - Башня Испытаний"""
    await message.answer(
        "🗼 <b>БАШНЯ ИСПЫТАНИЙ</b>\n\n"
        "🚧 100 этажей испытаний скоро откроются!\n\n"
        "Каждый этаж — новый вызов.\n"
        "Каждая победа — новая награда.\n\n"
        "Готовитесь к великим свершениям! ⚔️",
        parse_mode=ParseMode.HTML
    )