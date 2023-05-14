import threading
import datetime
import time

import sys, os

sys.path.append(
    os.path.abspath(
        os.path.join("..", "pythonBot\\python_bot\\test\\modules\\data\\dinamic\\")
    )
)
from load_db import (
    download_files_from_internet,
    load_db_from_local_files,
    check_csv_updated,
)


def update_database():
    download_files_from_internet()
    load_db_from_local_files()
    print("Updates completed")


def run_thread():
    if check_csv_updated():
        update_database()
    already_executed = False
    while True:
        now = datetime.datetime.now()
        if now.hour == 8 and now.minute == 10:
            if not already_executed:
                update_database()
                already_executed = True
        else:
            already_executed = False

        time.sleep(60)


def get_thread(already_started=False) -> threading.Thread:
    thread = threading.Thread(target=run_thread)
    if already_started:
        thread.start()
    return thread
