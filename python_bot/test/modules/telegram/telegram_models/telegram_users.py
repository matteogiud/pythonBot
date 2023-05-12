from ...data.dinamic.database_handle import *


class DbCar:
    def __init__(self, car_id: int, fuel_type, capacity, consume):
        self.car_id = car_id
        self.fuel_type = fuel_type
        self.capacity = capacity
        self.consume = consume


class DbTelgramUser:
    def __init__(self, chat_id: int, username: str, DbCar=None):
        self.chat_id = chat_id
        self.username = username
        self.DbCar = DbCar

    @staticmethod
    def get_by_chat_id(chat_id: int):
        db_user = get_telegram_user_from_db(chat_id)
        if (len(db_user) == 1):
            return DbTelgramUser(chat_id, db_user.username)
        return None

    @staticmethod
    def get_new_user(chat_id: int, username: str):
        db_user = create_new_user_in_db(chat_id, username)
        return DbTelgramUser(chat_id, None)
