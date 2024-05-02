import telegram
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = telegram.Bot(token=TOKEN)

bot.send_message(chat_id='@+IDlqK-7_W8ljMGVl', text='Hello World!!!')

# updater = telegram.ext.Updater(TOKEN, use_context=True)
# dispatch = updater.dispatcher

# def start(update, context):
#     update.message.reply_text("Hello! Welcom to telegram chat bot")

# def help(update, context):
#     update.message.reply_text(
#         """
#         Hi, here is Aaron, May I help you? Please type /start
#         """
#     )

# dispatch.add_handler(telegram.ext.CommandHandler('start', start))
# dispatch.add_handler(telegram.ext.CommandHandler('help', help))

# updater.start_polling()
# updater.idle()
