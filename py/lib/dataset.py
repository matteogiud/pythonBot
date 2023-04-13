import sqlite3
from typing import Type

class Database:    
    __instance = None
    __db_name = 'py\lib\data\database.db'
    __db_file_log = 'db_log.txt'
    
    @staticmethod
    def getInstance() -> Type['Database']:
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
        self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.fetchall()        
    
    def get_conn(self) -> Type['sqlite3.Connection']:
        return self.conn


    def __del__(self) -> None:
        """Distruttore che chiude la connessione al database"""
        self.conn.close()

    def __create_connection(self) -> sqlite3.Connection:
        from datetime import datetime
        try:
            print("Creating a database connection to a SQLite3 database")            
            conn = sqlite3.connect(self.__db_name)
            print('Connected')
            open(self.__db_file_log, mode='a').write('new connection: ' + str(datetime.now()) + '\n')
            return conn
        except Exception as e:
            print(e)
            return None