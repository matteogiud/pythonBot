from modules.data.dinamic.thread_routine_updates_database import get_thread, update_database
from modules.telegram.telegram import *
import time


# start thread update db
update_db_thread = get_thread()
update_db_thread.start()


# start my telegram server
my_telegram_token = "5783533607:AAE-4_vA8BZn5PGRjBvREylshRCyt42nRBY"
bot = Telegram(my_telegram_token, is_async=True)


@bot.handle_command("/start")
def handle_start_command(message: TelegramMessage):    
    text = f"""Benvenuto {message.user_from.username}!
        -Imposta il carburante: /setFuel
        -Imposta la capacità: /setCapacity"""
    

    response: TelegramResponse = TelegramResponse(message.chat.id, text)

    return response


@bot.handle_command("/setFuel")
def handle_set_fuel_command(message: TelegramMessage):

    text = "Scegli il carburante:"

    button_benzina = InlineKeyboardButton("BENZINA", callback_data='benzina')
    button_diesel = InlineKeyboardButton("GASOLIO", callback_data='gasolio')
    button_gpl = InlineKeyboardButton("GPL", callback_data='gpl')
    keyboard = InlineKeyboardMarkup(
        [[button_benzina, button_diesel, button_gpl]])

    response: TelegramResponse = TelegramResponse(
        message.chat.id, text, reply_markup=keyboard)

    # aggiunge un gestore riguardante quella chat e quella keyboard
    @bot.handle_callback_query(message.chat.id, keyboard)
    def set_fuel_callback_query(callback_query: TelegramCallbackQuery):
        response = TelegramResponse(
            callback_query.message.chat.id, "Carburante settato correttamente!")
        return response

    return response

@bot.handle_command("/setCapacity")
def handle_set_fuel_command(message: TelegramMessage):

    text = "Scegli il carburante:"

    button_benzina = InlineKeyboardButton("BENZINA", callback_data='benzina')
    button_diesel = InlineKeyboardButton("GASOLIO", callback_data='gasolio')
    button_gpl = InlineKeyboardButton("GPL", callback_data='gpl')
    keyboard = InlineKeyboardMarkup(
        [[button_benzina, button_diesel, button_gpl]])

    response: TelegramResponse = TelegramResponse(
        message.chat.id, text, reply_markup=keyboard)

    # aggiunge un gestore riguardante quella chat e quella keyboard
    @bot.handle_callback_query(message.chat.id, keyboard)
    def set_fuel_callback_query(callback_query: TelegramCallbackQuery):
        response = TelegramResponse(
            callback_query.message.chat.id, "Carburante settato correttamente!")
        return response

    return response

@bot.handle_command("/setConsume")
def handle_set_fuel_command(message: TelegramMessage):

    text = "Quanto consumi?"
    
    @bot.handle_next_message(message.chat.id) #da aggiungere
    def set_consume_callback(message: TelegramMessage):
        pass

    button_benzina = InlineKeyboardButton("BENZINA", callback_data='benzina')
    button_diesel = InlineKeyboardButton("GASOLIO", callback_data='gasolio')
    button_gpl = InlineKeyboardButton("GPL", callback_data='gpl')
    keyboard = InlineKeyboardMarkup(
        [[button_benzina, button_diesel, button_gpl]])

    response: TelegramResponse = TelegramResponse(
        message.chat.id, text, reply_markup=keyboard)

    # aggiunge un gestore riguardante quella chat e quella keyboard
    @bot.handle_callback_query(message.chat.id, keyboard)
    def set_fuel_callback_query(callback_query: TelegramCallbackQuery):
        response = TelegramResponse(
            callback_query.message.chat.id, "Carburante settato correttamente!")
        return response

    return response

@bot.handle_command("/help")
def handle_start_command(message: TelegramMessage):
    text = """- /setFuel per impostare il carburante della tua auto"""
    response: TelegramResponse = TelegramResponse(
        chat_id=message.chat_id, text=text)
    return response


bot.start_server(debug=True)
