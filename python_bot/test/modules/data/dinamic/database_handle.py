import sys, os; sys.path.append(os.path.abspath(os.path.join('..', 'pythonBot\\python_bot\\test\\modules\\data\\static\\')))
from dataset import Database # errore

global db
db = Database.getInstance()

def execute_insert_dict(table_name: str, data: list, table_values_names: tuple, dict_values_names: tuple):
    
    conn = db.get_conn()
    field_str = ", ".join(table_values_names)

    placeholders_str= ", ".join(["?" for _ in range(len(table_values_names))])

    for item in data:        
        values_str = ", ".join([str(item.get(field)) for field in dict_values_names])
        insert_query = f"INSERT INTO {table_name} ({field_str}) VALUES ({placeholders_str})"
        values_tuple = tuple(item.get(field) for field in dict_values_names)
        conn.execute(insert_query, values_tuple)

    conn.commit()
    
def delete_all_records_from_table(table_name: str):
    
    conn = db.get_conn()
    
    conn.execute(f"DELETE FROM {table_name} WHERE 1")
    
    conn.commit()