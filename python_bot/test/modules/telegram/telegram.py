import requests
import threading
import json
from time import sleep
from copy import deepcopy


class InlineKeyboardButton:
    def __init__(self, text, callback_data, request_location=False):
        self.text = text
        self.callback_data = callback_data
        self.request_location = request_location


class InlineKeyboardMarkup:
    def __init__(self, inline_keyboard):
        self.inline_keyboard = inline_keyboard


    def serialize_markup(self):
        serialized_buttons = []
        for row in self.inline_keyboard:
            serialized_row = []
            for button in row:
                serialized_row.append({'text': button.text,
                                       'callback_data': button.callback_data
                                       })
            serialized_buttons.append(serialized_row)

        return {'inline_keyboard': serialized_buttons}


class TelegramEntity:
    def __init__(self, entity: dict):
        self.type = entity.get("type") if entity.get("type") else None
        self.offset = entity.get("offset") if entity.get("offset") else None
        self.length = entity.get("length") if entity.get("length") else None


class TelegramUser:
    def __init__(self, user: dict):
        self.id = user.get("id") if user.get("id") else None
        self.is_bot = user.get("is_bot") if user.get(
            "is_bot") is not None else None
        self.first_name = user.get(
            "first_name") if user.get("first_name") else None
        self.username = user.get("username") if user.get("username") else None
        self.language_code = user.get(
            "language_code") if user.get("language_code") else None


class TelegramChat:
    def __init__(self, chat: dict):
        self.id = chat.get("id") if chat.get("id") else None
        self.first_name = chat.get(
            "first_name") if chat.get("first_name") else None
        self.username = chat.get("username") if chat.get("username") else None
        self.type = chat.get("type") if chat.get("type") else None


class TelegramReplyMarkup:

    def __init__(self, reply_markup: dict):
        inline_keyboard_markup = []
        inline_keyboard_rows = reply_markup.get(
            "inline_keyboard", [])
        if len(inline_keyboard_rows) > 0:
            for inline_keyboard_row in inline_keyboard_rows:
                inline_keyboard_markup.append([InlineKeyboardButton(
                    text=button["text"], callback_data=button["callback_data"]) for button in inline_keyboard_row])  # per ogni riga, aggiunge un vettore di inline keyboard button
        if len(inline_keyboard_markup) > 0:
            self.inline_keyboard_markup = InlineKeyboardMarkup(
                inline_keyboard_markup)
        else:
            self.inline_keyboard_markup = None


class TelegramMessage:
    def __init__(self, message: dict):
        self.message_id = message.get(
            "message_id") if message.get("message_id") else None
        self.user_from = TelegramUser(message.get(
            "from")) if message.get("from") else None
        self.chat = TelegramChat(message.get(
            "chat")) if message.get("chat") else None
        self.entities = TelegramEntities(message.get(
            "entities")) if message.get("entities") else None
        self.date = message.get("date") if message.get("date") else None
        self.text = message.get("text") if message.get("text") else None
        self.reply_markup = TelegramReplyMarkup(message.get(
            "reply_markup")) if message.get("reply_markup") else None

    def has_a_command(self):
        if self.entities is not None and len(self.entities.entities) > 0:
            for entity in self.entities.entities:
                if entity.type == "bot_command":
                    return True
        return False

    def get_command(self) -> str:
        if self.text is not None and self.text != "":
            for entity in self.entities.entities:
                if entity.type == "bot_command":
                    return self.text[entity.offset:entity.length]
        return None


class TelegramCallbackQuery:
    def __init__(self, callback_query: dict):
        self.id = callback_query.get(
            "id") if callback_query.get("id") else None
        self.user_from = TelegramUser(callback_query.get(
            "from")) if callback_query.get("from") else None
        self.message = TelegramMessage(callback_query.get(
            "message")) if callback_query.get("message") else None
        self.data = callback_query.get(
            "data") if callback_query.get("data") else None
        self.chat_instance = callback_query.get(
            "chat_instance") if callback_query.get("chat_instance") else None


class TelegramEntities:
    def __init__(self, entities: dict) -> None:
        self.entities = []
        for entity in entities:
            new_entity = TelegramEntity(entity)
            self.entities.append(new_entity)


class TelegramUpdate:  # il messaggio generale che arriva da un utente
    def __init__(self, update: dict):
        self.update_id = update.get("update_id")
        self.callback_query = TelegramCallbackQuery(update.get(
            "callback_query")) if update.get("callback_query") else None
        self.message = TelegramMessage(update.get(
            "message")) if update.get("message") else None

    # def has_a_command(self):
    #     for entity in self.entities:
    #         if entity.type == "bot_command":
    #             return True
    #     return False

    def is_a_message(self):
        return self.message is not None and self.callback_query is None

    def is_a_callback_query(self):
        return self.callback_query is not None and self.message is None


class TelegramResponse:
    def __init__(self, chat_id: int, text: str, reply_markup: InlineKeyboardMarkup = None):
        self.chat_id = chat_id
        self.text = text
        self.reply_markup = reply_markup

    def get_data(self) -> dict:
        data = {}
        print("chat_id", self.chat_id)
        data['chat_id'] = self.chat_id
        data['text'] = self.text
        if self.reply_markup is not None:
            data['reply_markup'] = self.reply_markup.serialize_markup()

        return data


class Telegram:
    def __init__(self, token, is_async=False):
        self.token = token
        self.url = f"https://api.telegram.org/bot{token}/"
        if is_async:
            self.server_thread = threading.Thread(target=self._server_polling)
        else:
            self.server_thread = None
        self.commands_handlers = {}
        self.callbacks_query_handlers = {}
        self.callbacks_next_message_handlers = {}
        self.update_offset = None
        self.debug = False

    def _server_polling(self):
        while True:
            updates = self.get_updates().get("result", [])
            for update in updates:
                req = TelegramUpdate(update)
                self._handler_dispatcher(req)
                print("UPDATE: ", update, "\r\n")

            sleep(1)

    def handle_next_message(self, chat_id: int, one_shot: bool = True):
        def decorator(func):
            # salvo l'id della chat e la keybord che gli è stata inviata
            self.callbacks_next_message_handlers[chat_id] = {
                "func": func, "one_shot": one_shot}  # salvo la func
            return func
        return decorator

    def handle_callback_query(self, chat_id, InlineKeyboardMarkup: InlineKeyboardMarkup, one_shot: bool = True):
        """Add an handler for a callback query"""
        def decorator(func):
            self.callbacks_query_handlers[chat_id] = {
                "func": func, "InlineKeyboardMarkup": InlineKeyboardMarkup, "one_shot": one_shot}  # salvo l'id della chat e la keybord che gli è stata inviata
            return func
        return decorator

    def _handler_dispatcher(self, update_message: TelegramUpdate):

        if update_message.is_a_message():  # se è un messaggio

            if self.callbacks_next_message_handlers.get(update_message.message.chat.id) is not None:
                func = self.callbacks_next_message_handlers.get(
                    update_message.message.chat.id)["func"]
                one_shot = self.callbacks_next_message_handlers.get(
                    update_message.message.chat.id)["one_shot"]

                threading.Thread(target=self.next_message_handler_wrapper, args=(
                    func, update_message.message, one_shot)).start()

            elif update_message.message.has_a_command():  # se la richiesta è un comando
                command = update_message.message.get_command()  # salvo il comando
                # se è presente un handler che gestisce il comando
                # prendo la funzione dal dizionario dei gestori
                func = self.commands_handlers.get(command)
                if func is not None:  # se c'è la funzione
                    print(f"GET command {command}")
                    # eseguo la funzione in un thread
                    threading.Thread(
                        target=self.command_handler_wrapper, args=(func, update_message.message)).start()

        # se è una callback query quindi è una risposta ad una inline keyboard
        elif update_message.is_a_callback_query():
            print(
                f"GET callback query /{update_message.callback_query.data}")
            handler_dict = self.callbacks_query_handlers.get(
                update_message.callback_query.message.chat.id)
            if handler_dict is not None:
                func = handler_dict["func"]
                one_shot = handler_dict["one_shot"]
                inlineKeyboardMarkup: InlineKeyboardMarkup = handler_dict["InlineKeyboardMarkup"]
                for inline_keyboard_row in inlineKeyboardMarkup.inline_keyboard:
                    for inline_button in inline_keyboard_row:
                        if inline_button.callback_data == update_message.callback_query.data:
                            threading.Thread(target=self.callback_query_handler_wrapper, args=(
                                func, update_message.callback_query)).start()  # eseguo un thread che fa partire una funzione passata come funzione e la TelegramCallbackQuery
                            break

        self.update_offset = update_message.update_id + 1

    def handle_command(self, command):
        """Add an handler for a command"""
        def decorator(func):
            self.commands_handlers[command] = func
            return func
        return decorator

    def start_server(self, debug=False):
        """Starts the server polling for updates, debug mode: print messages"""
        self.debug = debug
        if self.server_thread is None:
            self._server_polling()
        else:
            self.server_thread.start()

    def send_response(self, response: TelegramResponse):
        headers = {"Content-Type": "application/json"}
        url = self.url + "sendMessage"

        payload = response.get_data()
        print("payload", payload)
        result = requests.post(url, headers=headers, data=json.dumps(payload))
        print(result.json())

    def get_updates(self) -> dict:
        try:
            url = self.url + "getUpdates"
            params = {}
            if self.update_offset:
                params["offset"] = self.update_offset
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return None

    def command_handler_wrapper(self, func, message: TelegramMessage):
        response: TelegramResponse = func(message)
        print("command handler")
        if response is not None:
            self.send_response(response)

    def callback_query_handler_wrapper(self, func, message: TelegramCallbackQuery, one_shot=True):
        response: TelegramResponse = func(message)
        print("callback query handler")
        if response is not None:
            self.send_response(response)
        # elimino l'handler che è stato completato
        if one_shot:
            inlineKeyboard = self.callbacks_query_handlers[
                message.message.chat.id]["InlineKeyboardMarkup"].inline_keyboard

            if deepcopy(inlineKeyboard) == deepcopy(message.message.reply_markup.inline_keyboard_markup.inline_keyboard):
                del (self.callbacks_query_handlers[message.message.chat.id])
            else:
                print("skip")

    def next_message_handler_wrapper(self, func, message: TelegramMessage, one_shot=True):
        response: TelegramResponse = func(message)
        print("next message handler")
        if response is not None:
            self.send_response(response)

        if one_shot:
            del (self.callbacks_next_message_handlers[message.chat.id])
