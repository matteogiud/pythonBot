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

        return json.dumps({'inline_keyboard': serialized_buttons})


class TelegramEntity:
    def __init__(self, entity: dict):
        self.type = entity.get("type")
        self.offset = entity.get("offset")
        self.length = entity.get("length")


class TelegramUser:
    def __init__(self, user: dict):
        self.id = user.get("id")
        self.first_name = user.get("first_name")
        self.username = user.get("username")
        self.language_code = user.get("language_code")


class TelegramMessage:

    def __init__(self) -> None:
        pass


class TelegramCallbackQuery:
    def __init__(self, callback_query: dict):
        pass


class TelegramEntities:
    def __init__(self) -> None:
        pass


class TelegramUpdate:
    def __init__(self, update: dict):
        self.update_id = update.get("update_id")
        self.callback_query = TelegramCallbackQuery(update.get(
            "callback_query")) if update.get("callback_query") else None
        self.message = TelegramMessage(update.get(
            "message")) if update.get("message") else None
        self.entities = TelegramEntities(update.get(
            "entities")) if update.get("entities") else None

        entities = update.get('entities')
        for entity in entities:
            new_entity = TelegramEntity(entity)
            self.entities.append(new_entity)

        self.text = update.get("text")
        self.user_from = TelegramUser(message.get("from"))
        self.chat_id = update.get("chat").get("id")

    def parse_message(self, update):
        message = update.get('message')
        if 'message' in update:
            message = update['message']
            self.message_id = message.get('message_id')
            chat = message.get('chat')
            if chat:
                self.chat_id = chat.get('id')
            self.text = message.get('text')
        elif 'callback_query' in update:
            callback_query = update['callback_query']
            self.message_id = callback_query.get('message')['message_id']
            chat = callback_query.get('message')['chat']
            if chat:
                self.chat_id = chat.get('id')
            self.callback_data = callback_query.get('data')

    def has_a_command(self):
        for entity in self.entities:
            if entity.type == "bot_command":
                return True
        return False

    def get_data_json(self):
        data = {}
        data['chat_id'] = self.chat_id
        data['text'] = self.text
        data['reply_markup'] = self.reply_markup.serialize_markup(
        ) if self.reply_markup is not None else None

        return data


class TelegramResponse:
    def __init__(self, chat_id: int, text: str, reply_markup=None):
        self.chat_id = chat_id
        self.text = text
        self.reply_markup = reply_markup


class Telegram:
    def __init__(self, token, is_async=False):
        self.token = token
        self.url = f"https://api.telegram.org/bot{token}/"
        if is_async:
            self.server_thread = threading.Thread(target=self._server_polling)
        else:
            self.server_thread = None
        self.commands_handlers = {}
        self.update_offset = None
        self.debug = False

    def _server_polling(self):
        while True:
            updates = self.get_updates().get("result", [])
            for update in updates:
                # mess = TelegramMessage(update)
                print("UPDATE: ", update, "\r\n")

                # if mess.is_a_message() == True:
                #     if mess.has_a_command() == True:
                #         command = mess.text.split()[0].replace("/", "")
                #         if command in self.commands_handlers:
                #             print(f"GET /{command}\r\n")
                #             func = self.commands_handlers[command]
                #             # eseguo la funzione in un thread
                #             threading.Thread(
                #                 target=self.wrapper, args=(func, mess)).start()
                #     elif mess.is_a_callback_query() == True:
                #         print(f"GET /{callback_query['data']}\r\n")
                self.update_offset = update["update_id"] + 1
            sleep(1)

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
        result = requests.post(url, json=data)
        print(result.json())

    def get_updates(self):
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

    def wrapper(self, func, message):
        response: TelegramResponse = func(message)
        print("response: ", response)
        if response is not None:
            self.send_response(response)
