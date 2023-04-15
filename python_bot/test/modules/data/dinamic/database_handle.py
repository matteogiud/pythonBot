from dataset import Database  # errore
import sys
import os
sys.path.append(os.path.abspath(os.path.join(
    '..', 'pythonBot\\python_bot\\test\\modules\\data\\static\\')))

global db
db = Database.getInstance()


def execute_insert_dict(table_name: str, data: list, table_values_names: tuple, dict_values_names: tuple, db_table_log=None):

    from datetime import datetime

    conn = db.get_conn()
    field_str = ", ".join(table_values_names)

    placeholders_str = ", ".join(["?" for _ in range(len(table_values_names))])

    for item in data:
        values_str = ", ".join([str(item.get(field))
                               for field in dict_values_names])
        insert_query = f"INSERT INTO {table_name} ({field_str}) VALUES ({placeholders_str})"
        values_tuple = tuple(item.get(field) for field in dict_values_names)
        conn.execute(insert_query, values_tuple)

    conn.commit()

    if not db_table_log is None:
        open(db_table_log, 'a').write(
            f'{table_name} records loaded correctly: {datetime.now()}\n')


def delete_all_records_from_table(table_name: str):
    from datetime import datetime
    __db_deleting_logs = 'python_bot\\test\\data\\database\\logs\\db_delete_records.txt'
    conn = db.get_conn()

    conn.execute(f"DELETE FROM {table_name} WHERE 1")

    conn.commit()

    open(__db_deleting_logs, 'a').write(
        f'Delete all records from \'{table_name}\' table: {datetime.now()}\n')
