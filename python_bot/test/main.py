from modules.data.dinamic.thread_routine_updates_database import get_thread, update_database
from modules.telegram.telegram import *
from modules.telegram.define_handling import define_bot_handling
import time


# start thread update db
update_db_thread = get_thread()
update_db_thread.start()


# start my telegram server
my_telegram_token = "5783533607:AAE-4_vA8BZn5PGRjBvREylshRCyt42nRBY"
bot = Telegram(my_telegram_token, is_async=True)

define_bot_handling(bot)  

bot.start_server(debug=True)
