"""
Расчёты урона, опыта и повышений уровня
"""

import math
import random
from datetime import datetime


def calculate_damage(strength: int, agility: int, intelligence: int, weapon_damage: int = 0) -> int:
    """
    Расчёт урона персонажа
    
    Args:
        strength: Сила (главная характеристика для физ. урона)
        agility: Ловкость (влияет на крит. шанс)
        intelligence: Интеллект (маг. урон)
        weapon_damage: Урон от оружия
    
    Returns:
        Итоговый урон
    """
    # Базовый урон от характеристик
    physical_damage = strength * 1.5
    magical_damage = intelligence * 1.3
    agility_bonus = agility * 0.5
    
    base_damage = physical_damage + magical_damage + agility_bonus + weapon_damage
    
    # Случайность ±10%
    damage_variance = random.uniform(0.9, 1.1)
    
    # Шанс критического удара (5% + 0.5% за каждую единицу ловкости)
    crit_chance = 0.05 + (agility * 0.005)
    is_crit = random.random() < crit_chance
    
    if is_crit:
        base_damage *= 2.0  # Крит удваивает урон
    
    return int(base_damage * damage_variance)


def calculate_defense(defense: int, armor: int = 0) -> int:
    """
    Расчёт защиты персонажа
    
    Args:
        defense: Базовая защита
        armor: Защита от брони
    
    Returns:
        Итоговая защита
    """
    total_defense = defense + armor
    
    # Защита уменьшает урон на %
    # Формула: урон * (100 / (100 + защита))
    return total_defense


def calculate_exp_reward(base_exp: int, player_level: int, enemy_level: int = None) -> int:
    """
    Расчёт награды опыта
    
    Args:
        base_exp: Базовый опыт
        player_level: Уровень игрока
        enemy_level: Уровень врага (опционально)
    
    Returns:
        Итоговый опыт
    """
    exp = base_exp
    
    # Если указан уровень врага, учитываем разницу уровней
    if enemy_level:
        level_diff = enemy_level - player_level
        
        if level_diff > 0:
            # Враг сильнее - больше опыта
            exp = int(exp * (1 + level_diff * 0.1))
        elif level_diff < 0:
            # Враг слабее - меньше опыта
            penalty = max(0.1, 1 + level_diff * 0.15)  # Минимум 10% опыта
            exp = int(exp * penalty)
    
    return max(1, exp)  # Минимум 1 опыт


def calculate_exp_needed(level: int) -> int:
    """
    Расчёт опыта для следующего уровня
    
    Args:
        level: Текущий уровень
    
    Returns:
        Необходимый опыт для следующего уровня
    """
    # Экспоненциальная формула: базовый_опыт * (уровень ^ 1.5)
    base_exp = 100
    exp_needed = int(base_exp * math.pow(level, 1.5))
    
    return exp_needed


def check_level_up(player) -> bool:
    """
    Проверка и повышение уровня
    
    Args:
        player: Объект игрока
    
    Returns:
        True если был повышен уровень, False иначе
    """
    if player.exp >= player.exp_needed:
        # УРОВЕНЬ ПОВЫШЕН!
        player.level += 1
        player.exp = player.exp - player.exp_needed  # Остаток опыта
        player.exp_needed = calculate_exp_needed(player.level)
        
        # Награды за уровень
        player.max_hp += 10
        player.hp = player.max_hp  # Полное восстановление
        player.max_energy += 5
        player.energy = player.max_energy  # Полное восстановление
        
        # Очки характеристик
        player.stat_points += 3
        
        # Автоматическое распределение (можно убрать для ручного)
        player.strength += 2
        player.agility += 2
        player.intelligence += 2
        player.defense += 1
        
        # Награда монетами
        level_reward = player.level * 100
        player.coins += level_reward
        player.total_coins_earned += level_reward
        
        return True
    
    return False


def calculate_coin_reward(base_coins: int, luck: int = 0, multiplier: float = 1.0) -> int:
    """
    Расчёт награды монетами
    
    Args:
        base_coins: Базовая награда
        luck: Удача игрока (влияет на шанс бонуса)
        multiplier: Множитель (от событий, бустов)
    
    Returns:
        Итоговая награда
    """
    coins = base_coins
    
    # Случайность ±20%
    coins = int(coins * random.uniform(0.8, 1.2))
    
    # Шанс удачи (дополнительные 50% монет)
    luck_chance = 0.1 + (luck * 0.01)  # 10% + 1% за удачу
    if random.random() < luck_chance:
        coins = int(coins * 1.5)
    
    # Применяем множитель
    coins = int(coins * multiplier)
    
    return max(1, coins)


def calculate_pvp_rating_change(winner_rating: int, loser_rating: int, k_factor: int = 32) -> tuple[int, int]:
    """
    Расчёт изменения рейтинга в PvP (система Elo)
    
    Args:
        winner_rating: Рейтинг победителя
        loser_rating: Рейтинг проигравшего
        k_factor: K-фактор (чем выше, тем больше изменение)
    
    Returns:
        Кортеж (изменение_победителя, изменение_проигравшего)
    """
    # Ожидаемый результат
    expected_winner = 1 / (1 + math.pow(10, (loser_rating - winner_rating) / 400))
    expected_loser = 1 / (1 + math.pow(10, (winner_rating - loser_rating) / 400))
    
    # Изменение рейтинга
    winner_change = int(k_factor * (1 - expected_winner))
    loser_change = int(k_factor * (0 - expected_loser))
    
    return winner_change, loser_change


def calculate_guild_contribution(player_level: int, donation_amount: int) -> int:
    """
    Расчёт вклада игрока в гильдию
    
    Args:
        player_level: Уровень игрока
        donation_amount: Сумма пожертвования
    
    Returns:
        Очки вклада
    """
    # Базовые очки = сумма пожертвования
    contribution = donation_amount
    
    # Бонус за уровень (высокоуровневые игроки приносят больше пользы)
    level_bonus = 1 + (player_level * 0.01)  # +1% за уровень
    contribution = int(contribution * level_bonus)
    
    return contribution


def calculate_boss_damage_share(total_damage: int, player_damage: int, participant_count: int) -> float:
    """
    Расчёт доли урона игрока по боссу
    
    Args:
        total_damage: Общий урон всех участников
        player_damage: Урон игрока
        participant_count: Количество участников
    
    Returns:
        Доля урона (от 0 до 1)
    """
    if total_damage == 0:
        # Все участники получают равную долю
        return 1.0 / participant_count
    
    damage_share = player_damage / total_damage
    
    return damage_share


def calculate_tower_floor_difficulty(floor: int) -> dict:
    """
    Расчёт сложности этажа Башни Испытаний
    
    Args:
        floor: Номер этажа (1-100)
    
    Returns:
        Словарь с характеристиками этажа
    """
    # Экспоненциальный рост сложности
    base_hp = 100
    base_damage = 10
    base_exp = 50
    base_coins = 100
    
    multiplier = math.pow(1.15, floor)  # +15% за каждый этаж
    
    return {
        "floor": floor,
        "enemy_hp": int(base_hp * multiplier),
        "enemy_damage": int(base_damage * multiplier),
        "enemy_defense": int(floor * 2),
        "exp_reward": int(base_exp * multiplier),
        "coins_reward": int(base_coins * multiplier),
        "crystal_reward": floor // 10  # 1 кристалл каждые 10 этажей
    }


def calculate_daily_streak_bonus(streak_days: int) -> dict:
    """
    Расчёт бонуса за серию ежедневных входов
    
    Args:
        streak_days: Количество дней подряд
    
    Returns:
        Словарь с бонусами
    """
    base_coins = 100
    base_exp = 50
    
    # Бонус растёт с каждым днём
    multiplier = 1 + (streak_days * 0.1)  # +10% за каждый день
    
    # Максимальный множитель x3 (после 20 дней)
    multiplier = min(multiplier, 3.0)
    
    coins = int(base_coins * multiplier)
    exp = int(base_exp * multiplier)
    
    # Особые награды за вехи
    crystals = 0
    if streak_days == 7:
        crystals = 10
    elif streak_days == 14:
        crystals = 25
    elif streak_days == 30:
        crystals = 100
    
    return {
        "coins": coins,
        "exp": exp,
        "crystals": crystals,
        "multiplier": multiplier
    }


def calculate_item_upgrade_cost(item_level: int, rarity: str) -> int:
    """
    Расчёт стоимости улучшения предмета
    
    Args:
        item_level: Текущий уровень предмета
        rarity: Редкость (common, rare, epic, legendary)
    
    Returns:
        Стоимость в монетах
    """
    rarity_multiplier = {
        "common": 1.0,
        "rare": 2.0,
        "epic": 4.0,
        "legendary": 8.0
    }
    
    base_cost = 500
    multiplier = rarity_multiplier.get(rarity, 1.0)
    
    # Экспоненциальный рост стоимости
    cost = int(base_cost * multiplier * math.pow(1.5, item_level))
    
    return cost


def calculate_crafting_success_rate(player_level: int, recipe_level: int, luck: int = 0) -> float:
    """
    Расчёт шанса успешного крафта
    
    Args:
        player_level: Уровень игрока
        recipe_level: Требуемый уровень рецепта
        luck: Удача игрока
    
    Returns:
        Шанс успеха (от 0 до 1)
    """
    # Базовый шанс 50%
    base_chance = 0.5
    
    # Разница уровней
    level_diff = player_level - recipe_level
    level_bonus = level_diff * 0.05  # +5% за каждый уровень выше требуемого
    
    # Бонус от удачи
    luck_bonus = luck * 0.01  # +1% за единицу удачи
    
    success_rate = base_chance + level_bonus + luck_bonus
    
    # Ограничиваем от 10% до 95%
    success_rate = max(0.1, min(0.95, success_rate))
    
    return success_rate