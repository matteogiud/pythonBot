import sqlite3

global __conn
__conn = None


def get_db_instance(db_file) -> sqlite3.Connection:
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

get_db_instance(f"py\lib\data\database.db")
