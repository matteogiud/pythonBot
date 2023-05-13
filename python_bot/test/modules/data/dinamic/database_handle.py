from ..static.dataset import Database  # errore
import sys
import os
sys.path.append(os.path.abspath(os.path.join(
    '..', 'pythonBot\\python_bot\\test\\modules\\data\\static\\')))

global db
db = Database.getInstance()

# data manager


def execute_insert_dict(table_name: str, data: list, table_values_names: tuple, dict_values_names: tuple, db_table_log=None):

    from datetime import datetime

    conn = db.get_conn()
    field_str = ", ".join(table_values_names)

    placeholders_str = ", ".join(["?" for _ in range(len(table_values_names))])
    with Database.lock:
        for item in data:
            values_str = ", ".join([str(item.get(field))
                                    for field in dict_values_names])
            insert_query = f"INSERT INTO {table_name} ({field_str}) VALUES ({placeholders_str})"
            values_tuple = tuple(item.get(field)
                                 for field in dict_values_names)
            conn.execute(insert_query, values_tuple)

        conn.commit()

    if not db_table_log is None:
        open(db_table_log, 'a').write(
            f'{table_name} records loaded correctly: {datetime.now()}\n')


def delete_all_records_from_table(table_name: str):
    from datetime import datetime
    __db_deleting_logs = 'python_bot\\test\\data\\database\\logs\\db_delete_records.txt'
    conn = db.get_conn()
    with Database.lock:
        conn.execute(f"DELETE FROM {table_name} WHERE 1")
        conn.commit()

    open(__db_deleting_logs, 'a').write(
        f'Delete all records from \'{table_name}\' table: {datetime.now()}\n')


def get_telegram_user_from_db(chat_id: int):
    import sqlite3
    conn: sqlite3.Connection = db.get_conn()

    with Database.lock:
        user_cursor = conn.execute(
            "SELECT * FROM telegram_users LEFT JOIN cars ON telegram_users.car_id = cars.id WHERE chat_id = ?",
            (chat_id,)
        )
    rows = user_cursor.fetchall()

    column_names = [description[0] for description in user_cursor.description]

    user = [dict(zip(column_names, row)) for row in rows]

    return user


def create_new_user_in_db(chat_id: int, username: str):
    import sqlite3
    conn: sqlite3.Connection = db.get_conn()

    with Database.lock:
        res = conn.execute(
            "INSERT INTO telegram_users (chat_id, username) VALUES (?, ?)",
            (chat_id, username)
        )
        conn.commit()

    if res:
        return True
    return False


def create_new_car_in_db(chat_id: int):
    import sqlite3
    conn: sqlite3.Connection = db.get_conn()

    with Database.lock:
        new_car_id = conn.execute(
            "INSERT INTO cars (tipo_carburante, consumo_km_per_lt, capacita_serbatoio) VALUES (?, ?, ?)",
            (None, None, None)
        ).lastrowid
        conn.execute(
            "UPDATE telegram_users SET car_id = ? WHERE chat_id = ?",
            (new_car_id, chat_id)
        )
        conn.commit()

    return int(new_car_id)


def get_closer_gas_station_from_db(latitude: float, longitude: float):
    import sqlite3
    import math
    
    
    conn: sqlite3.Connection = db.get_conn()            


    

    with Database.lock:
        user_cursor = conn.execute(
            "SELECT *, ROUND(2 * 6371 * ASIN( SQRT( POWER( SIN((? - abs(latitudine)) * pi() / 180 / 2), 2) + COS(? * pi() / 180) * COS(abs(latitudine) * pi() / 180) * POWER( SIN((? - longitudine) * pi() / 180 / 2), 2))), 2) AS distance FROM installations ORDER BY distance LIMIT 5",
            (latitude, latitude, longitude)
        )
    rows = user_cursor.fetchall()

    column_names = [description[0] for description in user_cursor.description]

    installation = [dict(zip(column_names, row)) for row in rows]

    return installation


def set_fuel_type_in_db(car_id: int, fuel_type: str):
    import sqlite3
    conn: sqlite3.Connection = db.get_conn()

    with Database.lock:
        res = conn.execute(
            "UPDATE cars SET tipo_carburante = ? WHERE id = ?",
            (fuel_type, car_id)
        )
        conn.commit()

    if res:
        if res.rowcount > 0:
            return True

    return False


def set_capacity_in_db(car_id: int, capacity: str):
    import sqlite3
    conn: sqlite3.Connection = db.get_conn()

    with Database.lock:
        res = conn.execute(
            "UPDATE cars SET capacita_serbatoio = ? WHERE id = ?",
            (capacity, car_id)
        )
        conn.commit()

    if res:
        if res.rowcount > 0:
            return True

    return False


def set_consume_in_db(car_id: int, consume: str):
    import sqlite3
    conn: sqlite3.Connection = db.get_conn()

    with Database.lock:
        res = conn.execute(
            "UPDATE cars SET consumo_km_per_lt = ? WHERE id = ?",
            (consume, car_id)
        )
        conn.commit()

    if res:
        if res.rowcount > 0:
            return True

    return False
