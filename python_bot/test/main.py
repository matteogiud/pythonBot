from modules.data.dinamic.thread_routine_updates_database import get_thread, update_database
from modules.telegram.telegram import Telegram
import time


#start thread update db
update_db_thread = get_thread()
update_db_thread.start()




#start my telegram server
my_telegram_token = "5783533607:AAE-4_vA8BZn5PGRjBvREylshRCyt42nRBY"
my_telegram=Telegram(my_telegram_token)

my_telegram.start_server()

