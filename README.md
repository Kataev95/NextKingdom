# 🏰 NEXT KINGDOM - RPG BOT для Telegram

<tg-spoiler>**Полноценная RPG вселенная** для вашего чата The Next!</tg-spoiler>

Масштабный игровой бот с глубокой механикой, системой классов, гильдиями, боевой системой и захватывающей историей о спасении королевства от Тёмного Лорда.

---

## ✨ Возможности

### 🎭 Система Классов
- **6 уникальных классов** героев
- Воин, Лучник, Маг, Убийца, Паладин, Торговец
- Уникальные характеристики и бонусы

### 💰 Экономическая Система
- 3 вида валюты (Next Coins, Кристаллы, Осколки Силы)
- Работа, добыча ресурсов, ежедневные награды
- Магазин с оружием, бронёй и зельями
- Торговля между игроками

### ⚔️ Боевая Система
- PvE: Охота на 6+ видов монстров
- PvP: Дуэли с другими игроками
- Групповые рейды на боссов
- Башня Испытаний (100 этажей)

### 🏰 Гильдии
- Создание и управление гильдиями
- До 20 участников
- Общая казна и бонусы
- Войны между гильдиями

### 🌍 Мир и Локации
- 6 уникальных локаций
- Столица Некстград
- Тёмный Лес, Огненные Горы, Ледяные Пещеры
- Изумрудная Долина, Башня Испытаний

### 🎲 Случайные События
- Метеоритный дождь
- Счастливый час (x2 награды)
- Нашествие боссов
- Удачливый торговец

### 🏆 Достижения и Рейтинги
- 10+ базовых достижений
- Топы: по уровню, богатству, PvP, убийствам
- Рейтинг гильдий
- Награды за достижения

### 🎨 Новые Цветные Кнопки (Bot API 9.4)
- 🔵 Синие (Primary)
- 🟢 Зелёные (Success)
- 🔴 Красные (Danger)
- ⚪ Обычные

### 📖 Сюжет
- 10 глав истории
- Поиск фрагментов Кристалла Бесконечности
- Борьба с Тёмным Лордом Хаосом
- Уникальные персонажи и NPC

---

## 🚀 Установка и Запуск

### Требования
- **Python 3.10+**
- **Telegram Bot Token** (от [@BotFather](https://t.me/BotFather))
- **ID вашего чата** The Next

### Шаг 1: Клонирование
```bash
# Создайте папку проекта
mkdir next_kingdom_bot
cd next_kingdom_bot

# Скопируйте все файлы проекта в эту папку
```

### Шаг 2: Виртуальное окружение
```bash
# Создание venv
python3 -m venv venv

# Активация (Linux/Mac)
source venv/bin/activate

# Активация (Windows)
venv\\Scripts\\activate
```

### Шаг 3: Установка зависимостей
```bash
pip install -r requirements.txt
```

### Шаг 4: Настройка
Создайте файл `.env` в корне проекта:

```env
BOT_TOKEN=ваш_токен_от_BotFather
CHAT_ID=-1001234567890
DATABASE_URL=sqlite+aiosqlite:///next_kingdom.db
```

**Как получить CHAT_ID:**
1. Добавьте бота [@username_to_id_bot](https://t.me/username_to_id_bot) в ваш чат
2. Отправьте любое сообщение
3. Бот покажет ID чата (начинается с `-100`)

**Замените в config.py свой Telegram ID в списке ADMINS** (для админ-команд)

### Шаг 5: Структура проекта
```
next_kingdom_bot/
│
├── main.py                 # Точка входа
├── config.py               # Конфигурация
├── keyboards.py            # Клавиатуры с цветными кнопками
├── requirements.txt        # Зависимости
├── .env                    # Переменные окружения
│
├── database/
│   ├── __init__.py
│   ├── models.py          # Модели БД (SQLAlchemy)
│   └── database.py        # Работа с БД
│
├── handlers/              # Обработчики команд
│   ├── __init__.py
│   ├── start.py          # Старт и регистрация
│   ├── profile.py        # Профиль и статистика
│   ├── economy.py        # Экономика (work, daily, mine)
│   ├── combat.py         # Боевая система (hunt, pvp, raid)
│   ├── guild.py          # Гильдии
│   ├── events.py         # События
│   └── admin.py          # Админ-команды
│
└── utils/                # Вспомогательные утилиты
    ├── __init__.py
    ├── calculations.py   # Расчёты урона, опыта и т.д.
    ├── texts.py          # Текстовые шаблоны
    └── scheduler.py      # Планировщик событий
```

### Шаг 6: Создайте недостающие файлы

Создайте пустые `__init__.py`:
```bash
touch database/__init__.py
touch handlers/__init__.py
touch utils/__init__.py
```

### Шаг 7: Запуск бота
```bash
python main.py
```

При успешном запуске вы увидите:
```
🚀 Next Kingdom Bot запускается...
✅ База данных инициализирована
✅ Базовые достижения добавлены
⏰ Планировщик событий запущен
✅ Next Kingdom Bot успешно запущен!
```

---

## 📱 Команды Бота

### Основные
- `/start` - Регистрация / Возврат
- `/profile` - Ваш профиль
- `/help` - Справка по командам
- `/stats` - Подробная статистика

### Экономика
- `/work` - Работать (1 час кд)
- `/daily` - Ежедневная награда
- `/mine` - Добыча ресурсов (2 часа кд)
- `/shop` - Магазин
- `/balance` - Баланс

### Битвы
- `/hunt` - Охота на монстров
- `/pvp @username` - Дуэль с игроком
- `/raid` - Групповой рейд
- `/tower` - Башня Испытаний

### Гильдия
- `/guild` - Меню гильдии
- `/guild_create` - Создать гильдию
- `/guild_info` - Информация
- `/guild_leave` - Покинуть

### Информация
- `/inventory` - Инвентарь
- `/equipment` - Снаряжение
- `/top` - Рейтинги
- `/location` - Локация
- `/achievements` - Достижения
- `/events` - Активные события

---

## 🎮 Как Играть

### 1. Начало игры
1. Напишите `/start` в чате The Next
2. Выберите класс героя (6 вариантов)
3. Получите стартовые ресурсы и характеристики

### 2. Развитие персонажа
- Выполняйте `/work` каждый час
- Не забывайте `/daily` награду
- Охотьтесь на монстров `/hunt`
- Покупайте улучшения в `/shop`

### 3. Боевая система
- Начните с слабых монстров (Гоблин, Волк)
- Прокачивайтесь и сражайтесь с Драконами
- Участвуйте в PvP дуэлях
- Проходите Башню Испытаний

### 4. Социальные возможности
- Создайте или вступите в гильдию
- Участвуйте в групповых рейдах
- Соревнуйтесь в рейтингах
- Торгуйте с другими игроками

### 5. События
- Следите за случайными событиями
- Участвуйте для получения бонусов
- Еженедельные специальные дни (Понедельник - День Торговли, и т.д.)

---

## 🔧 Настройка

### Изменение игровых параметров

Отредактируйте `config.py`:

```python
# Стартовые ресурсы
START_COINS = 1000  # Измените на желаемое значение
START_LEVEL = 1

# Кулдауны (в секундах)
WORK_COOLDOWN = 3600  # 1 час
DAILY_COOLDOWN = 86400  # 24 часа

# Награды
WORK_REWARD_MIN = 100
WORK_REWARD_MAX = 300
DAILY_REWARD = 500
```

### Добавление новых монстров

В `config.py` раздел `MONSTERS`:

```python
"new_monster": {
    "name": "Новый Монстр",
    "emoji": "👾",
    "hp": 150,
    "damage": 25,
    "defense": 20,
    "exp_reward": 60,
    "coins_reward": (100, 250),
    "level_requirement": 8
}
```

### Добавление новых предметов

В `config.py` раздел `ITEMS`:

```python
"mythic_sword": {
    "name": "Мифический меч",
    "type": "weapon",
    "rarity": "mythic",
    "damage": 200,
    "price": 100000,
    "level_req": 50
}
```

---

## 🐛 Отладка и Логи

### Логи бота
Бот автоматически создаёт файл `bot.log` со всеми событиями:
```bash
tail -f bot.log
```

### Включить подробные SQL логи
В `database/database.py`:
```python
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Изменить на True
)
```

### Проверка базы данных
```bash
sqlite3 next_kingdom.db

# Посмотреть всех игроков
SELECT id, first_name, level, coins FROM players;

# Посмотреть гильдии
SELECT * FROM guilds;
```

---

## 🎨 Цветные Кнопки (Bot API 9.4)

Проект использует новейшую функцию Telegram Bot API 9.4:

```python
from aiogram.utils.keyboard import InlineKeyboardBuilder

builder = InlineKeyboardBuilder()

builder.button(
    text="✅ Подтвердить",
    callback_data="confirm",
    style="success"  # 🟢 Зелёная кнопка
)

builder.button(
    text="❌ Отмена",
    callback_data="cancel",
    style="danger"  # 🔴 Красная кнопка
)

builder.button(
    text="ℹ️ Информация",
    callback_data="info",
    style="primary"  # 🔵 Синяя кнопка
)
```

**Доступные стили:**
- `"primary"` - Синяя 🔵
- `"success"` - Зелёная 🟢
- `"danger"` - Красная 🔴
- `None` - Обычная ⚪

---

## 📊 База Данных

### Структура таблиц

**Players** - Игроки
- Характеристики, ресурсы, прогресс
- Класс героя, локация
- Статистика, кулдауны

**Guilds** - Гильдии
- Название, лидер, участники
- Казна, уровень, статистика

**Inventory** - Инвентарь игроков

**Equipment** - Экипированные предметы

**Achievements** - Достижения

**ActiveEvents** - Активные события

**Transactions** - История транзакций

**BattleLog** - Логи сражений

---

## 🚀 Деплой на Сервер

### На Ubuntu Server (ваш VPS)

1. **Подключитесь к серверу:**
```bash
ssh root@91.200.12.159
```

2. **Установите Python 3.10+:**
```bash
apt update
apt install python3.10 python3.10-venv python3-pip
```

3. **Загрузите проект:**
```bash
cd /root
mkdir next_kingdom_bot
cd next_kingdom_bot
# Загрузите файлы проекта
```

4. **Создайте venv и установите зависимости:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. **Создайте .env файл:**
```bash
nano .env
# Вставьте ваши настройки
```

6. **Запуск через systemd (автозапуск):**

Создайте `/etc/systemd/system/nextkingdom.service`:
```ini
[Unit]
Description=Next Kingdom Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/next_kingdom_bot
Environment="PATH=/root/next_kingdom_bot/venv/bin"
ExecStart=/root/next_kingdom_bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Команды управления:**
```bash
systemctl daemon-reload
systemctl start nextkingdom
systemctl enable nextkingdom  # Автозапуск
systemctl status nextkingdom  # Проверка статуса
systemctl restart nextkingdom  # Перезапуск
systemctl stop nextkingdom  # Остановка
```

**Просмотр логов:**
```bash
journalctl -u nextkingdom -f
```

---

## 📝 Разработка и Расширение

### Добавление нового обработчика

1. Создайте файл `handlers/my_feature.py`:
```python
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("mycommand"))
async def cmd_mycommand(message: Message):
    await message.answer("Моя новая команда!")
```

2. Зарегистрируйте в `main.py`:
```python
from handlers import my_feature

dp.include_router(my_feature.router)
```

### Добавление нового типа события

В `config.py` раздел `RANDOM_EVENTS`:
```python
"treasure_hunt": {
    "name": "🏴‍☠️ Поиск сокровищ",
    "description": "Найдите спрятанное сокровище первым!",
    "reward_coins": 1000,
    "reward_exp": 200,
    "duration": 900,  # 15 минут
    "max_participants": 5
}
```

---

## 💡 Советы и Трюки

### Оптимизация производительности
- Используйте индексы БД для частых запросов
- Кэшируйте данные игроков в Redis (опционально)
- Ограничивайте частоту команд (rate limiting)

### Безопасность
- Не делитесь `.env` файлом
- Регулярно делайте бэкапы базы данных
- Ограничьте админские команды

### Мониторинг
- Следите за логами бота
- Отслеживайте количество игроков
- Проверяйте использование ресурсов сервера

---

## 🤝 Поддержка и Вопросы

Если возникли проблемы:
1. Проверьте логи `bot.log`
2. Убедитесь, что все зависимости установлены
3. Проверьте правильность `.env` файла
4. Убедитесь, что бот добавлен в чат и имеет права администратора

---

## 📜 Лицензия

Проект создан специально для чата **The Next**.

Автор: **Amir Inc** 🚀

---

## 🎯 Roadmap (Будущие Обновления)

### Фаза 2: Морская Экспансия
- Новый регион: Острова Штормов
- Морские битвы и пиратские корабли
- Подводные сокровища

### Фаза 3: Небесные Врата
- Летающий город в облаках
- Новый класс: Небесный Рыцарь
- Воздушные сражения

### Фаза 4: Подземное Королевство
- Глубокие шахты с редкими рудами
- Гномья цивилизация
- Новые уникальные предметы

---

**🏰 Добро пожаловать в Next Kingdom! Да начнутся великие приключения!** ⚔️✨