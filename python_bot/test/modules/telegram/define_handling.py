from .telegram import *
from .telegram_models.telegram_users import DbTelgramUser


def define_bot_handling(bot: Telegram):

    # quando un utente starta il bot, controlla se l'utente è già presente nel db con i diversi settaggi,
    # altrimenti lo crea e gli dice di settare alcuni parametri attraverso una keyboard inline
    @bot.handle_command("/start")
    def handle_start_command(message: TelegramMessage):
        user: DbTelgramUser = DbTelgramUser.get_by_chat_id(message.chat.id) # salvo l'utente attuale
        if user is None:
            user = DbTelgramUser.get_new_user(message.chat.id, message.chat.username)

        
        text = f"""Benvenuto {message.user_from.username}!
            -Imposta il carburante: /setFuel
            -Imposta la capacità: /setCapacity"""

        response: TelegramResponse = TelegramResponse(message.chat.id, text)

        return response

    @bot.handle_command("/setFuel")
    def handle_set_fuel_command(message: TelegramMessage):

        text = "Scegli il carburante:"

        button_benzina = InlineKeyboardButton(
            "BENZINA", callback_data='benzina')
        button_diesel = InlineKeyboardButton(
            "GASOLIO", callback_data='gasolio')
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

        button_benzina = InlineKeyboardButton(
            "BENZINA", callback_data='benzina')
        button_diesel = InlineKeyboardButton(
            "GASOLIO", callback_data='gasolio')
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

        response: TelegramResponse = TelegramResponse(
            message.chat.id, text)

        @bot.handle_next_message(message.chat.id)  # da aggiungere
        def set_consume_callback(message: TelegramMessage):
            return TelegramResponse(message.chat.id, "Consumi settati!")

        return response

    @bot.handle_command("/help")
    def handle_start_command(message: TelegramMessage):
        text = """/setFuel per impostare il carburante della tua auto
    /setCapacity per impostare la capacità della tua auto
    /setConsume per impostare il consumo della tua auto"""
        response: TelegramResponse = TelegramResponse(
            chat_id=message.chat.id, text=text)
        return response
