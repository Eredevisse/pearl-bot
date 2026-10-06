import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8817688642:AAHxYYLbKnHYrKrQ-Uutllj-hoKjLv9-iT4"


async def get_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "pearl-2",
        "vs_currencies": "usd"
    }

    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    return data["pearl-2"]["usd"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💎 Pearl (PRL) бот работает!\n\n"
        "/price — текущая цена"
    )


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        prl_price = await get_price()

        await update.message.reply_text(
            f"💎 Pearl (PRL)\n"
            f"Цена: ${prl_price}"
        )

    except Exception:
        await update.message.reply_text("Не удалось получить цену PRL.")


async def hourly(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id

    try:
        prl_price = await get_price()

        await context.bot.send_message(
            chat_id=chat_id,
            text=f"💎 Pearl (PRL)\nЦена: ${prl_price}"
        )

    except Exception:
        pass


async def start_hourly(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Удаляем старую задачу, если она уже есть
    for job in context.job_queue.get_jobs_by_name(str(chat_id)):
        job.schedule_removal()

    # Отправка каждые 3600 секунд = 1 час
    context.job_queue.run_repeating(
        hourly,
        interval=3600,
        first=3600,
        chat_id=chat_id,
        name=str(chat_id)
    )

    await update.message.reply_text(
        "⏰ Готово! Цена PRL будет отправляться каждый час."
    )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("price", price))
app.add_handler(CommandHandler("hourly", start_hourly))

print("БОТ ЗАПУЩЕН")
app.run_polling()