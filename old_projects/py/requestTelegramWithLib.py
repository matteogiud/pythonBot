from lib.telegram import Telegram

telegram = Telegram("5783533607:AAE-4_vA8BZn5PGRjBvREylshRCyt42nRBY")
for message in telegram.getUpdate():
    print(message["message"]["text"])


