from .telegram import *
from .models.telegram_users import DbTelgramUser
from .models.gas_stations import DbGasStation


def get_inline_keyboard_set_command(user) -> TelegramInlineKeyboardMarkup:
    """user must be DbTelgramUser or user id"""
    GREEN_FLAG = "\U00002705"
    RED_CROSS = "\U0000274C"

    if isinstance(user, int):
        user = DbTelgramUser.get_by_id(user)

    if user is None or not isinstance(user, DbTelgramUser):
        return

    btnSetFuel = TelegramInlineKeyboardButton(
        text=(
            (RED_CROSS if user.DbCar.fuel_type is None else GREEN_FLAG)
            if user.DbCar is not None
            else RED_CROSS
        )
        + " Imposta il carburante",
        callback_data="setFuel",
    )
    btnSetCapacity = TelegramInlineKeyboardButton(
        text=(
            (RED_CROSS if user.DbCar.capacity is None else GREEN_FLAG)
            if user.DbCar is not None
            else RED_CROSS
        )
        + " Imposta la capacità",
        callback_data="setCapacity",
    )
    btnSetConsume = TelegramInlineKeyboardButton(
        text=(
            (RED_CROSS if user.DbCar.consume is None else GREEN_FLAG)
            if user.DbCar is not None
            else RED_CROSS
        )
        + " Imposta il consumo",
        callback_data="setConsume",
    )

    return TelegramInlineKeyboardMarkup(
        [[btnSetFuel], [btnSetCapacity], [btnSetConsume]]
    )


def define_bot_handling(bot: Telegram):
    GREEN_FLAG = "\U00002705"
    RED_CROSS = "\U0000274C"

    # quando un utente starta il bot, controlla se l'utente è già presente nel db con i diversi settaggi,
    # altrimenti lo crea e gli dice di settare alcuni parametri attraverso una keyboard inline
    @bot.handle_command("/start")
    def handle_start_command(message: TelegramMessage):
        text = f"Bentornato {message.chat.username}!"
        user: DbTelgramUser = DbTelgramUser.get_by_chat_id(
            message.chat.id
        )  # salvo l'utente attuale

        if user is None:  # se l'utente non è già presente
            user = DbTelgramUser.get_new_user(
                message.chat.id, message.chat.username if message.chat.username else message.chat.first_name
            )  # creo l'utente
            text = f"Benvenuto {message.chat.username}!"

        keyboard = get_inline_keyboard_set_command(user)

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
            message.chat.id, text, reply_markup=keyboard
        )

        return response

    @bot.handle_command("/setfuel")
    def handle_set_fuel_command(message: TelegramMessage):
        text = "Scegli il tipo di carburante \U000026FD"

        button_benzina = TelegramInlineKeyboardButton(
            "BENZINA", callback_data="BENZINA"
        )
        button_diesel = TelegramInlineKeyboardButton("GASOLIO", callback_data="GASOLIO")
        button_gpl = TelegramInlineKeyboardButton("GPL", callback_data="GPL")
        keyboard = TelegramInlineKeyboardMarkup(
            [[button_benzina, button_diesel, button_gpl]]
        )

        response: TelegramResponse = TelegramResponse(
            message.chat.id, text, reply_markup=keyboard
        )

        # aggiunge un gestore riguardante quella chat e quella keyboard
        @bot.handle_callback_query(message.chat.id, keyboard)
        def set_fuel_callback_query(callback_query: TelegramCallbackQuery):
            text = "Carburante settato correttamente!"
            try:
                data = callback_query.data
                user = DbTelgramUser.get_by_chat_id(
                    message.chat.id
                )  # salvo l'utente attuale

                if user.DbCar is None:
                    user.create_new_car()  # creo una nuova macchina

                if not user.DbCar.set_fuel_type(data):
                    raise Exception

            except:
                text = "Errore!"

            # TODO SEND KEYBOARD WHEN SET FUEL

            response = TelegramResponse(callback_query.message.chat.id, text)
            return response

        return response

    @bot.handle_command("/setcapacity")
    def handle_set_capacity_command(message: TelegramMessage):
        text = "Invia la capacità del serbatoio della tua auto"

        response: TelegramResponse = TelegramResponse(message.chat.id, text)

        @bot.handle_next_message(message.chat.id)
        def set_capacity_callback_message(callback_message: TelegramMessage):
            text = "Capacità settata correttamente!"
            try:
                data = callback_message.text
                user = DbTelgramUser.get_by_chat_id(
                    message.chat.id
                )  # salvo l'utente attuale

                if user.DbCar is None:
                    user.create_new_car()  # creo una nuova macchina

                if not user.DbCar.set_capacity(data):
                    raise Exception

            except:
                text = "Capacità non valida!"

            response = TelegramResponse(callback_message.chat.id, text)
            return response

        return response

    @bot.handle_command("/setconsume")
    def handle_set_consume_command(message: TelegramMessage):
        text = "Invia il consumo medio della tua auto"

        response: TelegramResponse = TelegramResponse(message.chat.id, text)

        @bot.handle_next_message(message.chat.id)
        def set_capacity_callback_message(callback_message: TelegramMessage):
            text = "Consumo medio settato correttamente!"
            try:
                data = callback_message.text
                user = DbTelgramUser.get_by_chat_id(
                    message.chat.id
                )  # salvo l'utente attuale

                if user.DbCar is None:
                    user.create_new_car()  # creo una nuova macchina

                if not user.DbCar.set_consume(data):
                    raise Exception

            except:
                text = "Consumo medio non valido!"

            response = TelegramResponse(callback_message.chat.id, text)
            return response

        return response

    @bot.handle_command("/getgasstation")
    def handle_get_gasstation_command(message: TelegramMessage):
        
        user:DbTelgramUser=DbTelgramUser.get_by_chat_id(message.chat.id)
        
        if user.DbCar is None or not user.DbCar.is_setted_correctly():
            return TelegramResponse(message.chat.id, """Per continuare prima devi impostare correttamente il profilo
    - /setfuel
    - /setcapacity
    - /setconsume""")
            
            
        text = "Scegli il risultato che vuoi visualizzare"
        keyboard = None

        if message.location is None:
            text = "Condividimi la tua posizione attuale per continuare..."
            request_position_telegram = TelegramCustomButton(
                text=text, request_location=True
            )
            keyboard = TelegramCustomKeyboard(
                [[request_position_telegram]],
                resize_keyboard=False,
                one_time_keyboard=True,
            )

            @bot.handle_next_message(message.chat.id)
            def check_location_callback_message(callback_message: TelegramMessage):
                return handle_get_gasstation_command(callback_message)

        else:  # quando la posizione mi è stata fornita
            btn_closer_results = TelegramInlineKeyboardButton(
                text="Più Vicini", callback_data="closer_results"
            )
            btn_cheaper_results = TelegramInlineKeyboardButton(
                text="Più Convenienti", callback_data="cheaper_results"
            )
            keyboard = TelegramInlineKeyboardMarkup(
                [[btn_closer_results], [btn_cheaper_results]]
            )

            @bot.handle_callback_query(message.chat.id, keyboard)
            def calculate_result(callback_query: TelegramCallbackQuery):
                if callback_query.data == "closer_results":
                    stations = DbGasStation.get_closer_gas_stations(
                        message.location.latitude,
                        message.location.longitude,
                        user
                    )
                    for station in stations:
                        bot.send_location(
                            message.chat.id,
                            location=TelegramLocation(
                                {
                                    "latitude": station.latitudine,
                                    "longitude": station.longitudine,
                                }
                            ),
                            title=f"{station.nome_impianto}: {station.selfPrice}€-litro",
                        )

                    return
                elif callback_query.data == "cheaper_results":
                    callback_text = "Quanti litri di carburante devi fare?"

                    @bot.handle_next_message(message.chat.id)
                    def get_liters_callback_message(callback_message: TelegramMessage):
                        try:
                            if not callback_message.text.isdigit():
                                raise Exception("Valore non valido")

                            user = DbTelgramUser.get_by_chat_id(message.chat.id)

                            liters = int(callback_message.text)
                            if liters < 0 or liters > user.DbCar.capacity:
                                raise Exception("Valore non valido")
                                # valore valido

                            bot.send_response(
                                TelegramResponse(
                                    message.chat.id,
                                    "Sto calcolando i migliori benzinai nella tua zona...",
                                )
                            )

                            stations = DbGasStation.get_cheaper_gas_stations(
                                message.location.latitude,
                                message.location.longitude,
                                liters,
                                user,
                            )  # get the cheaper stations
                            for station in stations:
                                bot.send_location(
                                    message.chat.id,
                                    location=TelegramLocation(
                                        {
                                            "latitude": station.latitudine,
                                            "longitude": station.longitudine,
                                        }
                                    ),
                                    title=f"{station.nome_impianto}: {station.selfPrice}€-litro",
                                )

                            return

                        except Exception as e:
                            return TelegramResponse(message.chat.id, e.args[0])

                    return TelegramResponse(message.chat.id, callback_text)
                return

        if keyboard:
            return TelegramResponse(message.chat.id, text, reply_markup=keyboard)
        else:
            return TelegramResponse(message.chat.id, text)
