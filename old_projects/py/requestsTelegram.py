import requests
import time

token = "5783533607:AAE-4_vA8BZn5PGRjBvREylshRCyt42nRBY"
URL = f"https://api.telegram.org/bot{token}/"

servizio = "getUpdates"
servizioSend = "sendMessage"

while True:
    response = requests.get(URL+servizio)
    if response.status_code == 200:
        responseJson = response.json()
        # print(responseJson)
        if responseJson["ok"]:
            for messaggio in responseJson["result"]:
                text = messaggio["message"]["text"]
                if str(messaggio["message"]["text"]).lower().find("ciao") != -1:
                    text = "ciao anche a te!"                

                chatId = messaggio["message"]["chat"]["id"]
                if requests.post(URL+servizioSend, data={"chat_id": chatId, "text": text}).status_code == 200:
                    print("risposta inviata")
                    requests.get(
                        URL+servizio, params={"offset": int(messaggio["update_id"])+1})

            # listaMessaggi = [str(m["message"]["text"]) for m in responseJson["result"]]
    else:
        print("error")
    time.sleep(1)