import requests
import threading
from time import sleep


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
                    chat_id = message["chat"]["id"]
                    text = message.get("text")
                    print(f"from {chat_id}: {text}")
                    if text:
                        command = text.split()[0].replace("/", "")
                        if command in self.commands_handlers:
                            print(f"GET /{command}")
                            func = self.commands_handlers[command]
                            func(chat_id, text)
                self.update_offset = update["update_id"] + 1
            sleep(1)

    def handle_command(self, command):
        def decorator(func):
            self.commands_handlers[command] = func
            return func
        return decorator

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

    def send_message(self, chat_id, text):
        url = self.url + "sendMessage"
        data = {"chat_id": chat_id, "text": text}
        response = requests.post(url, json=data)
        return response.json()

    def get_updates(self):
        url = self.url + "getUpdates"
        params = {}
        if self.update_offset:
            params["offset"] = self.update_offset
        response = requests.get(url, params=params)
        return response.json()

