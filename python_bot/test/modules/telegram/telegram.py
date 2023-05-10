import requests
import threading
import json
from time import sleep



class TelegramMessage:
    def __init__(self, message: dict):
        self.message_id = message.get("message_id")
        self.date = message.get("date")
        self.entities = []

        entities = message.get('entities')
        for entity in entities:
            new_entity = TelegramEntity(entity)
            self.entities.append(new_entity)

        self.text = message.get("text")
        self.user_from = TelegramUser(message.get("from"))
        self.chat_id = message.get("chat").get("id")

    def has_a_command(self):
        for entity in self.entities:
            if entity.type == "bot_command":
                return True
        return False


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


class TelegramResponse:
    def __init__(self, chat_id: int, text: str):
        self.chat_id = chat_id
        self.text = text

    def get_data_json(self):
        data = {}
        data['chat_id'] = self.chat_id
        data['text'] = self.text
        
        return data

class Telegram:

    def __init__(self, token, is_async=False):
        self.token = token
        self.url = f"https://api.telegram.org/bot{token}/"
        if is_async:
            self.server_thread = threading.Thread(target=self.server_handle)
        else:
            self.server_thread = None
        self.commands_handlers = {}
        self.update_offset = None
        self.debug = False

    def server_handle(self):
        while True:
            updates = self.get_updates().get("result", [])
            for update in updates:
                message = update.get("message")
                if message:
                    mess = TelegramMessage(message)
                    print(f"new message from {mess}")
                    if mess.has_a_command() == True:
                        command = mess.text.split()[0].replace("/", "")
                        if command in self.commands_handlers:
                            print(f"GET /{command}")
                            func = self.commands_handlers[command]
                            # eseguo la funzione in un thread
                            threading.Thread(
                                target=self.wrapper, args=(func, mess)).start()
                self.update_offset = update["update_id"] + 1
            sleep(1)

    def handle_command(self, command):
        def decorator(func):

            self.commands_handlers[command] = func
            return func
        return decorator

    def wrapper(self, func, message):
        response: TelegramResponse = func(message)
        print("response: ", response)
        if response is not None:
            self.send_response(response)

    def start_server(self, debug=False):
        self.debug = debug
        if self.server_thread is None:
            self.server_handle()
        else:
            self.server_thread.start()

    def getUpdates(self, params={}, setOffset=True):
        urlUpdate = self.url + "getUpdates"
        try:
            response = requests.get(urlUpdate, params)
            response.raise_for_status()

            responseJson = response.json()
            messageList = []

            offsetId = -1
            for messaggio in responseJson["result"]:
                messageList.append(messaggio)
                offsetId = messaggio["update_id"]
            offsetId += 1
            if setOffset:
                requests.get(urlUpdate+"getUpdates",
                             params={"offset": offsetId})

        except Exception as e:
            messageList = None
            print(f"Error: {e}")

        return messageList

    def send_text_message(self, chat_id, text=None):
        url = self.url + "sendMessage"
        data = {"chat_id": chat_id, "text": text}
        response = requests.post(url, json=data)
        return response.json()

    def send_response(self, response: TelegramResponse):
        url = self.url + "sendMessage"
        data = response.get_data_json()
        print("data: ", data)
        result = requests.post(url, json=data)
        print(result.json())

    def get_updates(self):
        url = self.url + "getUpdates"
        params = {}
        if self.update_offset:
            params["offset"] = self.update_offset

        response = requests.get(url, params=params)
        return response.json()