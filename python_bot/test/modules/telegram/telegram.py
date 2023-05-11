import requests
import threading
import json
from time import sleep


class InlineKeyboardButton:
    def __init__(self, text, callback_data):
        self.text = text
        self.callback_data = callback_data


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
        self.inline_keyboard_buttons = [InlineKeyboardButton(
            text=button["text"], callback_data=button["callback_data"]) for button in reply_markup.get("inline_keyboard", [])]


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
        for entity in self.entities.entities:
            if entity.type == "bot_command":
                return True

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
    def __init__(self, chat_id: int, text: str, reply_markup: InlineKeyboardMarkup=None):
        self.chat_id = chat_id
        self.text = text
        self.reply_markup = reply_markup
        
    def get_data_json(self):
        data = {}
        print("chat_id", self.chat_id)
        data['chat_id'] = self.chat_id if self.chat_id is not None else None
        data['text'] = self.text if self.text is not None else None
        data['reply_markup'] = self.reply_markup.serialize_markup(
        ) if self.reply_markup is not None else None

        return json.dumps(data)
        


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

    def handle_callback_query(self, chat_id, InlineKeyboardMarkup: InlineKeyboardMarkup):
        """Add an handler for a callback query"""
        def decorator(func):
            self.callbacks_query_handlers[chat_id] = {
                "func":func, "InlineKeyboardMarkup": InlineKeyboardMarkup}  # salvo l'id della chat e la keybord che gli è stata inviata
            return func
        return decorator

    def _handler_dispatcher(self, update_message: TelegramUpdate):
        def dispatch(self, update_message: TelegramUpdate):
            if update_message.is_a_message():  # se è un messaggio
                if update_message.message.has_a_command():  # se la richiesta è un comando
                    command = update_message.message.get_command()  # salvo il comando
                    # se è presente un handler che gestisce il comando
                    # prendo la funzione dal dizionario dei gestori
                    func = self.commands_handlers.get(command)
                    if func is not None:  # se c'è la funzione
                        print(f"GET command {command}")
                        # eseguo la funzione in un thread
                        threading.Thread(
                            target=self.command_handler_wrapper, args=(func, update_message.message)).start()
                        return

            # se è una callback query quindi è una risposta ad una inline keyboard
            elif update_message.is_a_callback_query():
                print(f"GET callback query /{update_message.callback_query.data}")
                handler_dict = self.callbacks_query_handlers.get(update_message.callback_query.message.chat.id)
                if handler_dict is not None:
                    func = handler_dict["func"]
                    inlineKeyboardMarkup: InlineKeyboardMarkup = handler_dict["InlineKeyboardMarkup"]
                    for inline_button in inlineKeyboardMarkup.inline_keyboard:
                        if inline_button.callback_data == update_message.callback_query.data:
                            threading.Thread(target=self.callback_query_handler_wrapper, args=(handler_dict, update_message.callback_query)).start()
                            return
                    

            self.update_offset = update_message.update_id + 1

        # threading.Thread(target=dispatch, args=(
        #     self, update_message)).start()
        dispatch(self, update_message)

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

    # def send_text_message(self, chat_id, text=None):
    #     url = self.url + "sendMessage"
    #     data = {"chat_id": chat_id, "text": text}
    #     response = requests.post(url, json=data)
    #     return response.json()

    def send_response(self, response: TelegramResponse):
        url = self.url + "sendMessage"

        data = response.get_data_json()
        print("data: ", data)
        result = requests.post(url, data=data)
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

    def callback_query_handler_wrapper(self, func, message: TelegramCallbackQuery):
        response: TelegramResponse = func(message)
        print("callback query handler")
        if response is not None:
            self.send_response(response)
        # elimino l'handler che è stato completato
        del (self.callbacks_query_handlers[message.message.chat.id])
