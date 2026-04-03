# Lachesis

Минималистичный Telegram-бот бинарной дивинации.

Один вопрос → один квантовый жребий: **да** или **нет**.

Источник случайности — [Outshift QRNG](https://qrng.outshift.com/): физический квантовый шум, не алгоритм.

---

## Структура

```
bot/
├── config.py          — загрузка конфигурации из .env
├── texts.py           — весь копирайт
├── handlers/
│   ├── start.py       — /start, /help
│   └── divination.py  — основной сценарий гадания
└── services/
    └── quantum.py     — абстракция RandomProvider + Outshift QRNG
run.py                 — точка входа
```

## Запуск

```bash
# 1. Клонировать репозиторий
git clone <url>
cd lachesis

# 2. Создать виртуальное окружение
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
.venv\Scripts\activate         # Windows

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Настроить переменные окружения
cp .env.example .env
# Открыть .env и вписать реальные токены

# 5. Запустить
python run.py
```

## Переменные окружения

| Переменная     | Описание                             |
|----------------|--------------------------------------|
| `BOT_TOKEN`    | Токен Telegram-бота (от @BotFather)  |
| `QRNG_API_KEY` | API-ключ Outshift QRNG               |

## Команды бота

| Команда  | Описание                  |
|----------|---------------------------|
| `/start` | Начало, кнопка жребия     |
| `/help`  | Краткое описание механики |
