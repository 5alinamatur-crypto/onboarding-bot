import csv
import time
from datetime import datetime
import pytz

from telegram.ext import Updater, CommandHandler

TOKEN = "8210005594:AAEjGcw4gmbI1o_xV8UcxkVD20C-6ugvat0"

moscow = pytz.timezone("Europe/Moscow")


def load_schedule():
    with open("schedule.csv") as f:
        return list(csv.DictReader(f))


def load_chats():
    try:
        with open("chats.csv") as f:
            return list(csv.DictReader(f))
    except:
        return []


def save_chat(chat_id, start_date):

    chats = load_chats()

    chats.append({
        "chat_id": chat_id,
        "start_date": start_date
    })

    with open("chats.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["chat_id", "start_date"])
        writer.writeheader()
        writer.writerows(chats)


def addchat(update, context):

    chat_id = update.effective_chat.id

    try:
        start_date = context.args[0]
    except:
        update.message.reply_text("Напиши дату: /addchat 2026-03-20")
        return

    save_chat(chat_id, start_date)

    update.message.reply_text("Чат добавлен 🚀")


def scheduler(bot):

    while True:

        now = datetime.now(moscow)

        chats = load_chats()
        schedule = load_schedule()

        for chat in chats:

            start_date = datetime.strptime(chat["start_date"], "%Y-%m-%d")

            day_number = (now.date() - start_date.date()).days + 1

            for item in schedule:

                if int(item["day"]) == day_number:

                    hour, minute = item["time"].split(":")

                    if now.hour == int(hour) and now.minute == int(minute):

                        bot.send_message(
                            chat_id=int(chat["chat_id"]),
                            text=item["message"]
                        )

        time.sleep(60)


def main():

    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("addchat", addchat))

    updater.start_polling()

    scheduler(updater.bot)


if __name__ == "__main__":
    main()