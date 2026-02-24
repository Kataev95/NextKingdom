# 🏰 NEXT KINGDOM - ПОЛНАЯ ИНСТРУКЦИЯ ПО УСТАНОВКЕ

## 📦 ВСЕ СОЗДАННЫЕ ФАЙЛЫ (17 ФАЙЛОВ)

### Основные файлы:
1. `main.py` - Главный файл запуска
2. `config.py` - Конфигурация (классы, монстры, предметы, цветные кнопки)
3. `keyboards.py` - Клавиатуры с цветными кнопками
4. `requirements.txt` - Базовые зависимости
5. `requirements-full.txt` - Полные зависимости с APScheduler
6. `.env.example` - Пример настроек
7. `next-kingdom-lore.md` - Полная вселенная и история
8. `README.md` - Документация

### База данных:
9. `database/models.py` - 9 моделей БД
10. `database/database.py` - Работа с БД

### Обработчики:
11. `handlers/start.py` - Регистрация, выбор класса
12. `handlers/economy.py` - Экономика (work, daily, mine)
13. `handlers/combat.py` - Боевая система (hunt, pvp, raid)
14. `handlers/guild.py` - Гильдии
15. `handlers/events.py` - Случайные события
16. `handlers/admin.py` - Админ-команды

### Утилиты:
17. `utils/scheduler.py` - Планировщик событий
18. `utils/calculations.py` - Расчёты урона/опыта

---

## 🚀 ПОШАГОВАЯ УСТАНОВКА

### ШАГ 1: Создайте структуру папок

```bash
# Перейдите в домашнюю директорию
cd /root

# Создайте главную папку проекта
mkdir next_kingdom_bot
cd next_kingdom_bot

# Создайте подпапки
mkdir database
mkdir handlers
mkdir utils

# Создайте пустые __init__.py файлы
touch database/__init__.py
touch handlers/__init__.py
touch utils/__init__.py
```

### ШАГ 2: Разместите файлы по папкам

**Корневая директория** (`/root/next_kingdom_bot/`):
```
main.py
config.py
keyboards.py
requirements.txt
requirements-full.txt
.env
next-kingdom-lore.md
README.md
```

**Папка database/**:
```
database/__init__.py
database/models.py
database/database.py
```

**Папка handlers/**:
```
handlers/__init__.py
handlers/start.py          (переименуйте handler-start.py)
handlers/economy.py        (переименуйте handler-economy.py)
handlers/combat.py         (переименуйте handler-combat.py)
handlers/guild.py          (переименуйте handler-guild.py)
handlers/events.py         (переименуйте handler-events.py)
handlers/admin.py          (переименуйте handler-admin.py)
```

**Папка utils/**:
```
utils/__init__.py
utils/scheduler.py         (переименуйте utils-scheduler.py)
utils/calculations.py      (переименуйте utils-calculations.py)
```

### ШАГ 3: Переименуйте файлы

После скачивания файлов с дефисами, переименуйте их:

```bash
# В папке handlers/
mv handler-start.py start.py
mv handler-economy.py economy.py
mv handler-combat.py combat.py
mv handler-guild.py guild.py
mv handler-events.py events.py
mv handler-admin.py admin.py

# В папке utils/
mv utils-scheduler.py scheduler.py
mv utils-calculations.py calculations.py
```

### ШАГ 4: Создайте .env файл

```bash
nano .env
```

Вставьте и настройте:
```env
# Токен бота от @BotFather
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# ID чата The Next (начинается с -100)
CHAT_ID=-1001234567890

# База данных (SQLite по умолчанию)
DATABASE_URL=sqlite+aiosqlite:///next_kingdom.db

# Логирование
LOG_LEVEL=INFO
```

**Как узнать ID чата:**
1. Добавьте бота @username_to_id_bot в ваш чат
2. Отправьте любое сообщение
3. Бот покажет ID чата (например: -1001234567890)

### ШАГ 5: Обновите config.py

Откройте `config.py` и настройте:

```python
# Ваш Telegram ID для админ-доступа
ADMIN_IDS = [
    123456789,  # Замените на свой ID
]
```

**Как узнать свой ID:**
- Напишите боту @userinfobot
- Он покажет ваш ID

### ШАГ 6: Установите зависимости

```bash
# Активируйте виртуальное окружение (если есть)
cd /root/next_kingdom_bot
python3 -m venv venv
source venv/bin/activate

# Установите полные зависимости (с планировщиком)
pip install -r requirements-full.txt

# Или базовые (без автоматических событий)
# pip install -r requirements.txt
```

### ШАГ 7: Проверьте структуру

Финальная структура должна выглядеть так:

```
next_kingdom_bot/
│
├── main.py
├── config.py
├── keyboards.py
├── requirements.txt
├── requirements-full.txt
├── .env
├── next-kingdom-lore.md
├── README.md
│
├── database/
│   ├── __init__.py
│   ├── models.py
│   └── database.py
│
├── handlers/
│   ├── __init__.py
│   ├── start.py
│   ├── economy.py
│   ├── combat.py
│   ├── guild.py
│   ├── events.py
│   └── admin.py
│
└── utils/
    ├── __init__.py
    ├── scheduler.py
    └── calculations.py
```

### ШАГ 8: Запустите бота

```bash
python main.py
```

Вы должны увидеть:
```
INFO - Инициализация базы данных...
INFO - База данных инициализирована!
INFO - Планировщик событий запущен
INFO - Бот запущен! Нажмите Ctrl+C для остановки
```

---

## 🎮 ДОСТУПНЫЕ КОМАНДЫ

### Для всех игроков:

**📝 Основные:**
- `/start` - Регистрация и выбор класса
- `/profile` - Ваш профиль
- `/help` - Список команд

**💰 Экономика:**
- `/work` - Работа (каждые 30 минут)
- `/daily` - Ежедневная награда (24 часа)
- `/mine` - Добыча ресурсов (1 час)
- `/shop` - Магазин
- `/inventory` - Инвентарь

**⚔️ Боевая система:**
- `/hunt` - Охота на монстров (20 минут, 20 энергии)
- `/pvp` - Дуэль с игроком (30 минут, 30 энергии)
- `/raid` - Групповой рейд (в разработке)
- `/tower` - Башня Испытаний (в разработке)

**🏰 Гильдии:**
- `/guild` - Меню гильдии
- `/guild_create <название>` - Создать гильдию (10,000 монет)
- `/guild_info` - Информация о гильдии
- `/guild_leave` - Покинуть гильдию
- `/guild_donate <сумма>` - Пожертвовать в казну

**🎲 События:**
- `/events` - Активные события
- `/catch` - Поймать метеорит (во время события)
- `/boss_attack` - Атаковать босса (во время события)

**📊 Рейтинги:**
- `/top` - Топ игроков
- `/leaderboard` - Таблица лидеров

### Для администраторов:

**👑 Админ-панель:**
- `/admin` - Панель администратора
- `/stats` - Статистика бота
- `/give_coins @user <кол-во>` - Выдать монеты
- `/give_crystals @user <кол-во>` - Выдать кристаллы
- `/set_level @user <уровень>` - Установить уровень
- `/spawn_event <тип>` - Запустить событие
- `/broadcast <текст>` - Рассылка сообщения
- `/reset_cooldowns @user` - Сбросить кулдауны

**Типы событий для spawn_event:**
- `meteor_shower` - Метеоритный дождь
- `lucky_merchant` - Удачливый торговец
- `happy_hour` - Счастливый час
- `boss_raid` - Нашествие боссов

---

## 🤖 АВТОМАТИЧЕСКИЕ СОБЫТИЯ (Планировщик)

Если вы установили `requirements-full.txt`, планировщик автоматически:

### Каждую минуту:
- ⚡ Восстанавливает 1 энергию всем игрокам

### Каждые 5 минут:
- ❤️ Восстанавливает 5 HP всем игрокам
- 🧹 Очищает истёкшие события

### Каждые 2 часа:
- 🎲 Запускает случайное событие (30% шанс)

### Каждый день (00:00 UTC):
- 🌅 Сбрасывает ежедневные лимиты
- 📢 Уведомляет игроков

### Каждую неделю (понедельник 00:00):
- 🏆 Награждает топ-10 игроков
- 📊 Сбрасывает недельные рейтинги

### Каждые 6 часов:
- 📡 Логирует статус сервера

---

## 🔧 НАСТРОЙКА SYSTEMD (Автозапуск)

Чтобы бот запускался автоматически при перезагрузке сервера:

### 1. Создайте systemd сервис:

```bash
sudo nano /etc/systemd/system/nextkingdom.service
```

### 2. Вставьте конфигурацию:

```ini
[Unit]
Description=Next Kingdom RPG Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/next_kingdom_bot
ExecStart=/root/next_kingdom_bot/venv/bin/python main.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### 3. Активируйте сервис:

```bash
# Перезагрузите systemd
sudo systemctl daemon-reload

# Включите автозапуск
sudo systemctl enable nextkingdom

# Запустите сервис
sudo systemctl start nextkingdom

# Проверьте статус
sudo systemctl status nextkingdom

# Просмотр логов
sudo journalctl -u nextkingdom -f
```

### 4. Управление сервисом:

```bash
# Остановить
sudo systemctl stop nextkingdom

# Перезапустить
sudo systemctl restart nextkingdom

# Отключить автозапуск
sudo systemctl disable nextkingdom
```

---

## 🎨 ЦВЕТНЫЕ КНОПКИ (Bot API 9.4)

Бот использует **новую функцию Telegram** - цветные кнопки!

### Доступные стили:

```python
# В файле keyboards.py
builder.button(
    text="💼 Работать",
    callback_data="economy:work",
    style="success"  # 🟢 Зелёная кнопка
)

builder.button(
    text="⚔️ Охота",
    callback_data="combat:hunt",
    style="primary"  # 🔵 Синяя кнопка
)

builder.button(
    text="❌ Выход",
    callback_data="guild:leave",
    style="danger"  # 🔴 Красная кнопка
)

builder.button(
    text="ℹ️ Информация",
    callback_data="info",
    style=None  # ⚪ Обычная кнопка
)
```

---

## 💾 РЕЗЕРВНОЕ КОПИРОВАНИЕ

### Создание бэкапа базы данных:

```bash
# Ручной бэкап
cp next_kingdom.db next_kingdom_backup_$(date +%Y%m%d).db

# Автоматический бэкап каждый день в 03:00
crontab -e
```

Добавьте строку:
```
0 3 * * * cp /root/next_kingdom_bot/next_kingdom.db /root/next_kingdom_bot/backups/backup_$(date +\%Y\%m\%d).db
```

### Восстановление из бэкапа:

```bash
# Остановите бота
sudo systemctl stop nextkingdom

# Восстановите базу
cp next_kingdom_backup_20260224.db next_kingdom.db

# Запустите бота
sudo systemctl start nextkingdom
```

---

## 📊 МОНИТОРИНГ

### Просмотр логов в реальном времени:

```bash
# Если запущен через systemd
sudo journalctl -u nextkingdom -f

# Если запущен вручную, логи в файле
tail -f logs/bot.log  # если настроено логирование в файл
```

### Проверка работы бота:

```bash
# Статус сервиса
sudo systemctl status nextkingdom

# Проверка процесса
ps aux | grep main.py

# Проверка использования ресурсов
top -p $(pgrep -f main.py)
```

---

## 🐛 TROUBLESHOOTING

### Бот не запускается:

**1. Проверьте .env файл:**
```bash
cat .env
```
Убедитесь что BOT_TOKEN и CHAT_ID правильные

**2. Проверьте зависимости:**
```bash
pip list | grep aiogram
pip list | grep SQLAlchemy
pip list | grep APScheduler
```

**3. Проверьте импорты:**
```bash
python -c "import aiogram; print('OK')"
python -c "import sqlalchemy; print('OK')"
```

### База данных не создаётся:

```bash
# Удалите старую БД
rm next_kingdom.db

# Запустите бота снова
python main.py
```

### Планировщик не работает:

```bash
# Проверьте установку APScheduler
pip install APScheduler

# Проверьте логи на ошибки
grep "scheduler" logs/bot.log
```

### Бот не отвечает в чате:

1. Проверьте что бот добавлен в чат
2. Проверьте права бота (должен быть админом)
3. Проверьте CHAT_ID в .env
4. Проверьте что команды пишутся с `/`

---

## 📚 ДОПОЛНИТЕЛЬНЫЕ РЕСУРСЫ

- **Документация Aiogram 3:** https://docs.aiogram.dev/
- **Telegram Bot API:** https://core.telegram.org/bots/api
- **SQLAlchemy 2.0:** https://docs.sqlalchemy.org/
- **APScheduler:** https://apscheduler.readthedocs.io/

---

## 🎯 СЛЕДУЮЩИЕ ШАГИ

1. ✅ Установите и запустите базовую версию
2. ✅ Протестируйте команды в чате
3. 🔄 Добавьте дополнительные обработчики (по желанию)
4. 🎨 Настройте дизайн сообщений
5. 📊 Настройте мониторинг и логирование
6. 🚀 Запустите для игроков!

---

## 🤝 ПОДДЕРЖКА

Если возникли вопросы или проблемы, проверьте:
1. Логи бота
2. Правильность установки всех файлов
3. Настройки .env
4. Версии зависимостей

**Удачи с Next Kingdom! ⚔️✨**