import requests

class Telegram:

    def __init__(self, token):
        self.url = f"https://api.telegram.org/bot{token}/"

    def getUpdate(self, params={}, setOffset=True):
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
            offsetId+=1
            if setOffset:
                requests.get(urlUpdate+"getUpdates", params={"offset": offsetId})

        except Exception as e:
            messageList = None
            print(f"Error: {e}")

        return messageList

    def sendMessage(self, message):
        urlSendMessage = self.url + "sendMessage"

t = Telegram("5783533607:AAE-4_vA8BZn5PGRjBvREylshRCyt42nRBY")
print(t.getUpdate())
