import sqlite3
from typing import Type
import threading
import math
import os
import sys
# sys.path.append(
#     os.path.abspath(
#         os.path.join("..", "pythonBot\\python_bot\\test\\modules\\telegram\\")
#     )
# )
from ...telegram.open_route_service import get_route_distance


def cheap_ratio(route_distance: float, prezzo_self: float, lt_to_do: int, avg_consume: float) -> float:
    """restituisce il prezzo totale per fare benzina in un certo posto"""
    try:
        consume_price = ((route_distance / 1000)/ avg_consume ) * prezzo_self
        price_to_do = prezzo_self * lt_to_do
        return consume_price + price_to_do
    except:
        return None


class Database:
    __instance = None
    lock = threading.Lock()
    __db_name = "test\\data\\database\\database.db"
    __db_file_log = "test\\data\\database\\logs\\db_log.txt"

    @staticmethod
    def getInstance() -> Type["Database"]:
        """Restituisce l'istanza del singleton"""
        if Database.__instance == None:
            Database()
        return Database.__instance

    def __init__(self) -> None:
        """Costruttore privato che inizializza il database"""
        if Database.__instance != None:
            raise Exception("Questa è una classe singleton!")
        else:
            self.conn = self.__create_connection()
            self.cursor = self.conn.cursor()
            Database.__instance = self

    def execute(self, query, params) -> list:
        """Esegue una query SQL"""
        with Database.lock:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.fetchall()

    def get_conn(self) -> Type["sqlite3.Connection"]:
        return self.conn

    def __del__(self) -> None:
        """Distruttore che chiude la connessione al database"""
        self.conn.close()

    def __create_connection(self) -> sqlite3.Connection:
        from datetime import datetime

        try:
            print("Creating a database connection to a SQLite3 database")
            conn = sqlite3.connect(self.__db_name, check_same_thread=False)

            conn.create_function("SQRT", 1, math.sqrt)
            conn.create_function("ASIN", 1, math.asin)
            conn.create_function("POWER", 2, math.pow)
            conn.create_function("COS", 1, math.cos)
            conn.create_function("SIN", 1, math.sin)
            conn.create_function("ROUTEDISTANCE", 4, get_route_distance)
            conn.create_function("CHEAPRATIO", 4, cheap_ratio)
            conn.create_function("pi", 0, lambda: math.pi)

            print("Connected")
            open(self.__db_file_log, mode="a").write(
                "new connection: " + str(datetime.now()) + "\n"
            )
            return conn
        except Exception as e:
            print(e)
            return None
