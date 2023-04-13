from dataset import * # errore
global db
db = Database.getInstance()

def execute_insert_dict(table_name: str, data: list, table_values_names: tuple, dict_values_names: tuple):
    
    conn = db.get_conn()
    field_str = ", ".join(table_values_names)

    placeholders_str= ", ".join(["?" for _ in range(len(table_values_names))])

    for item in data:        
        values_str = ", ".join([str(data.get(field)) for field in dict_values_names])
        insert_query = f"INSERT INTO {table_name} ({field_str}) VALUES ({placeholders_str})"
        values_tuple = tuple(data.get(field) for field in dict_values_names)
        #conn.execute(insert_query, values_tuple)

    # conn.commit()