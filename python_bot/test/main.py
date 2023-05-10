from modules.data.dinamic.thread_routine_updates_database import get_thread, update_database
from modules.telegram.telegram import *
import time


#start thread update db
update_db_thread = get_thread()
update_db_thread.start()




#start my telegram server
my_telegram_token = "5783533607:AAE-4_vA8BZn5PGRjBvREylshRCyt42nRBY"
bot=Telegram(my_telegram_token, is_async=True)

@bot.handle_command("start")
def handle_start_command(message: TelegramMessage):
    text = f"Benvenuto ciccio {message.chat_id}"
    response:TelegramResponse = TelegramResponse(message.chat_id, text)
    
    
    return response


@bot.handle_command("help")
def handle_start_command(message: TelegramMessage):
    bot.send_text_message(chat_id=message.chat_id, text="Ti aiuto")
    return 



bot.start_server(debug=True)

