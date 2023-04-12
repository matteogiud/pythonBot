import sqlite3

class handle_db:
    global __conn
    __conn = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(handle_db, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        

    def get_db_instance(self, db_file) -> sqlite3.Connection:
        global __conn
        if __conn == None:
            __conn = create_connection(db_file)
        return __conn


    def create_connection(db_file) -> sqlite3.Connection:
        try:
            print("Creating a database connection to a SQLite3 database")
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
            return conn
        except Exception as e:
            print(e)
            return None

db = handle_db()
db.get_db_instance(f"py\lib\data\database.db")
