global downloading_folder
downloading_folder = 'python_bot\\test\\data\\csv_files\\'



def download_files_from_internet():
    import requests
    from datetime import datetime
    fuel_price_link = 'https://www.mise.gov.it/images/exportCSV/prezzo_alle_8.csv'
    installations_link = 'https://www.mise.gov.it/images/exportCSV/anagrafica_impianti_attivi.csv'
    
    __fuel_price_log = 'python_bot\\test\\data\\csv_files\\logs\\fuel_price_log.txt'
    __installations_log = 'python_bot\\test\\data\\csv_files\\logs\\installations_log.txt'

    response = requests.get(fuel_price_link)
    if response.status_code == 200:
        with open(f'{downloading_folder}fuel_price.csv', 'wb') as file:
            file.write(response.content)
        open(__fuel_price_log, 'a').write(
            f'Downloaded \'fuel_price.csv\': {str(datetime.now())}\n')

    response = requests.get(installations_link)
    if response.status_code == 200:
        with open(f'{downloading_folder}installations.csv', 'wb') as file:
            file.write(response.content)
            open(__installations_log, 'a').write(
            f'Downloaded \'installations.csv\': {str(datetime.now())}\n')


def load_db_from_local_files(delete_table_first=True):
    import sys
    import os
    from datetime import datetime
    sys.path.append(os.path.abspath(os.path.join(
        '..', 'pythonBot\\python_bot\\test\\modules\\data\\static\\')))
    from csv_parser import parse_dict
    
    from database_handle import execute_insert_dict, delete_all_records_from_table

    __db_fuel_price_log = 'python_bot\\test\\data\\database\\logs\\db_fuel_price.txt'
    __db_installations_log = 'python_bot\\test\\data\\database\\logs\\db_installations.txt'
    
    
    fuel_price_dict = parse_dict(
        f'{downloading_folder}fuel_price.csv', no_first=1)
    installations_dict = parse_dict(
        f'{downloading_folder}installations.csv', no_first=1)

    fuel_price_dict = clean_fuel_price_dict(fuel_price_dict)
    installations_dict = clean_installations_dict(installations_dict)

    if delete_table_first:
        delete_all_records_from_table(table_name='installations')
        delete_all_records_from_table(table_name='fuel_prices')

    execute_insert_dict('installations', installations_dict, ('id', 'latitudine', 'longitudine', 'nome_impianto',
                        'bandiera', 'indirizzo', 'comune', 'provincia'), ('idImpianto', 'Latitudine', 'Longitudine', 'Nome Impianto', 'Bandiera', 'Indirizzo', 'Comune', 'Provincia'), __db_installations_log)
    print('Installations records loaded correctly')

    execute_insert_dict('fuel_prices', fuel_price_dict, ('idImpianto',
                        'tipoCarburante', 'prezzoSelf'), ('idImpianto', 'descCarburante', 'prezzo'), __db_fuel_price_log)
    print('Fuel prices records loaded correctly')


def clean_fuel_price_dict(fuel_price_dict: list) -> list:

    def get_fuel_type(fuel_type: str) -> str:
        real_fuel_type: str = None

        if fuel_type.lower().find('benz') != -1:
            real_fuel_type = 'BENZINA'
        elif fuel_type.lower().find('dies') != -1:
            real_fuel_type = 'GASOLIO'
        elif fuel_type.lower().find('gpl') != -1:
            real_fuel_type = 'GPL'

        return real_fuel_type

    new_fuel_price_dict = []

    for item in fuel_price_dict:
        if item['isSelf'] == '0':
            continue

        fuel_type = get_fuel_type(item['descCarburante'])

        if fuel_type is None:
            continue

        new_fuel_price_dict.append(
            {'idImpianto': item['idImpianto'], 'descCarburante': fuel_type, 'prezzo': item['prezzo']})

    return new_fuel_price_dict


def clean_installations_dict(installations_dict: list) -> list:
    new_installations_dict = []

    for item in installations_dict:
        installation = {
            'idImpianto': item['idImpianto'],
            'Latitudine': item['Latitudine'],
            'Longitudine': item['Longitudine'],
            'Nome Impianto': None if str(item['Nome Impianto']).lower() == 'null' else item['Nome Impianto'],
            'Bandiera': None if str(item['Bandiera']).lower() == 'null' else item['Bandiera'],
            'Indirizzo': None if str(item['Indirizzo']).lower() == 'null' else item['Indirizzo'],
            'Comune': None if str(item['Comune']).lower() == 'null' else item['Comune'],
            'Provincia': None if (str(item['Provincia']).lower() == 'null' or len(item['Provincia']) > 2) else item['Provincia']
        }

        new_installations_dict.append(installation)

    return new_installations_dict

