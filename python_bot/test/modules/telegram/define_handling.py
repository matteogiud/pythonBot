from .telegram import *
from .telegram_models.telegram_users import DbTelgramUser


def define_bot_handling(bot: Telegram):

    GREEN_FLAG = "\U00002705"
    RED_CROSS = "\U0000274C"

    # quando un utente starta il bot, controlla se l'utente è già presente nel db con i diversi settaggi,
    # altrimenti lo crea e gli dice di settare alcuni parametri attraverso una keyboard inline
    @bot.handle_command("/start")
    def handle_start_command(message: TelegramMessage):
        text = f"Bentornato {message.chat.username}!"
        user: DbTelgramUser = DbTelgramUser.get_by_chat_id(
            message.chat.id)  # salvo l'utente attuale

        if user is None:  # se l'utente non è già presente
            user = DbTelgramUser.get_new_user(
                message.chat.id, message.chat.username)  # creo l'utente
            text = f"Benvenuto {message.chat.username}!"

        btnSetFuel = InlineKeyboardButton(
            text=((RED_CROSS if user.DbCar.fuel_type is None else GREEN_FLAG) if user.DbCar is not None else RED_CROSS) + " Imposta il carburante", callback_data='setFuel')
        btnSetCapacity = InlineKeyboardButton(
            text=((RED_CROSS if user.DbCar.capacity is None else GREEN_FLAG) if user.DbCar is not None else RED_CROSS) + " Imposta la capacità", callback_data='setCapacity')
        btnSetConsume = InlineKeyboardButton(
            text=((RED_CROSS if user.DbCar.consume is None else GREEN_FLAG) if user.DbCar is not None else RED_CROSS) + " Imposta il consumo", callback_data='setConsume')

        keyboard = InlineKeyboardMarkup(
            [[btnSetFuel], [btnSetCapacity], [btnSetConsume]]
        )

        @bot.handle_callback_query(message.chat.id, keyboard)
        def send_to_relative_command(callback_query: TelegramCallbackQuery):
            response = None
            if callback_query.data == "setFuel":
                response = handle_set_fuel_command(message)
            elif callback_query.data == "setCapacity":
                response = handle_set_capacity_command(message)
            elif callback_query.data == "setConsume":
                response = handle_set_consume_command(message)
            return response

    # """-Imposta il carburante: /setFuel
    # -Imposta la capacità: /setCapacity
    # -Imposta il consumo: /setConsume"""

        response: TelegramResponse = TelegramResponse(
            message.chat.id, text, reply_markup=keyboard)

        return response

    @bot.handle_command("/setFuel")
    def handle_set_fuel_command(message: TelegramMessage):

        text = "Scegli il tipo di carburante \U000026FD"

        button_benzina = InlineKeyboardButton(
            "BENZINA", callback_data='BENZINA')
        button_diesel = InlineKeyboardButton(
            "GASOLIO", callback_data='GASOLIO')
        button_gpl = InlineKeyboardButton("GPL", callback_data='GPL')
        keyboard = InlineKeyboardMarkup(
            [[button_benzina, button_diesel, button_gpl]])

        response: TelegramResponse = TelegramResponse(
            message.chat.id, text, reply_markup=keyboard)

        # aggiunge un gestore riguardante quella chat e quella keyboard
        @bot.handle_callback_query(message.chat.id, keyboard)
        def set_fuel_callback_query(callback_query: TelegramCallbackQuery):
            text = "Carburante settato correttamente!"
            try:
                data = callback_query.data
                user = DbTelgramUser.get_by_chat_id(
                    message.chat.id)  # salvo l'utente attuale

                if user.DbCar is None:
                    user.create_new_car()  # creo una nuova macchina

                if not user.DbCar.set_fuel_type(data):
                    raise Exception

            except:
                text = "Errore!"

            response = TelegramResponse(
                callback_query.message.chat.id, text)
            return response

        return response

    @bot.handle_command("/setCapacity")
    def handle_set_fuel_command(message: TelegramMessage):

        text = "Invia la capacità del serbatoio della tua auto"

        response: TelegramResponse = TelegramResponse(
            message.chat.id, text)

        @bot.handle_next_message(message.chat.id)
        def set_capacity_callback_message(callback_message: TelegramMessage):
            text = "Capacità settata correttamente!"
            try:
                data = callback_message.text
                user = DbTelgramUser.get_by_chat_id(
                    message.chat.id)  # salvo l'utente attuale

                if user.DbCar is None:
                    user.create_new_car()  # creo una nuova macchina

                if not user.DbCar.set_capacity(data):
                    raise Exception

            except:
                text = "Capacità non valida!"

            response = TelegramResponse(
                callback_message.chat.id, text)
            return response

        return response

    @bot.handle_command("/setConsume")
    def handle_set_fuel_command(message: TelegramMessage):

        text = "Invia il consumo medio della tua auto"

        response: TelegramResponse = TelegramResponse(
            message.chat.id, text)

        @bot.handle_next_message(message.chat.id)
        def set_capacity_callback_message(callback_message: TelegramMessage):
            text = "Consumo medio settato correttamente!"
            try:
                data = callback_message.text
                user = DbTelgramUser.get_by_chat_id(
                    message.chat.id)  # salvo l'utente attuale

                if user.DbCar is None:
                    user.create_new_car()  # creo una nuova macchina

                if not user.DbCar.set_consume(data):
                    raise Exception

            except:
                text = "Consumo medio non valido!"

            response = TelegramResponse(
                callback_message.chat.id, text)
            return response

        return response
