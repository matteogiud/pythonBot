from ...data.dinamic.database_handle import (
    set_capacity_in_db,
    set_consume_in_db,
    set_fuel_type_in_db,
    get_telegram_user_from_db,
    create_new_car_in_db,
    create_new_user_in_db
)


class DbCar:
    def __init__(self, car_id: int, fuel_type, capacity, consume):
        self.car_id = car_id
        self.fuel_type = fuel_type
        self.capacity = capacity
        self.consume = consume

    def set_fuel_type(self, fuel_type):
        if fuel_type in ("BENZINA", "GASOLIO", "GPL"):
            if set_fuel_type_in_db(self.car_id, fuel_type) is not None:
                self.fuel_type = fuel_type
                return True
        return False

    def set_capacity(self, capacity):
        if int(capacity) > 0:
            if set_capacity_in_db(self.car_id, capacity) is not None:
                self.capacity = capacity
                return True
        return False

    def set_consume(self, consume):
        if int(consume) > 0:
            if set_consume_in_db(self.car_id, consume) is not None:
                self.capacity = consume
                return True
        return False
    
    def is_setted_correctly(self):
        return self.fuel_type is not None and self.capacity is not None and self.consume is not None


class DbTelgramUser:
    def __init__(self, chat_id: int, username: str, DbCar=None):
        self.chat_id = chat_id
        self.username = username
        self.DbCar: DbCar = DbCar

    def create_new_car(self):
        db_car_id = create_new_car_in_db(self.chat_id)
        if db_car_id is not None:
            self.DbCar = DbCar(db_car_id, None, None, None)

    @staticmethod
    def get_by_chat_id(chat_id: int):
        db_user = get_telegram_user_from_db(chat_id)
        if len(db_user) == 1:
            if db_user[0]["car_id"] is not None:
                return DbTelgramUser(
                    chat_id,
                    db_user[0]["username"],
                    DbCar(
                        db_user[0]["car_id"],
                        db_user[0]["tipo_carburante"],
                        db_user[0]["capacita_serbatoio"],
                        db_user[0]["consumo_km_per_lt"],
                    ),
                )
            else:
                return DbTelgramUser(chat_id, db_user[0]["username"])
        return None

    @staticmethod
    def get_new_user(chat_id: int, username: str):
        if create_new_user_in_db(chat_id, username):
            return DbTelgramUser(chat_id, username)
        else:
            return None



