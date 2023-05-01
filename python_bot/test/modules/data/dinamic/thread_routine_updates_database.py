import threading
import datetime
import time

import sys, os; sys.path.append(os.path.abspath(os.path.join(
        '..', 'pythonBot\\python_bot\\test\\modules\\data\\dinamic\\')))
from load_db import download_files_from_internet, load_db_from_local_files


def update_database():
    download_files_from_internet()
    load_db_from_local_files()
    print('Updates completed')

def run_thread():
    already_executed = False
    while True:
        now = datetime.datetime.now()
        if now.hour == 8 and now.minute == 10:
            if not already_executed:
                update_database()
                already_executed = False
        else:
            already_executed = False

        time.sleep(60)

def get_thread(already_started=False) -> threading.Thread:
    thread = threading.Thread(target=run_thread)
    if already_started:
        thread.start()
    return thread
