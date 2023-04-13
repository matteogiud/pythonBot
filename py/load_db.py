global downloading_folder
downloading_folder = 'py\\csvfiles\\'

def download_files_from_internet():
    import requests
    fuel_price_link = 'https://www.mise.gov.it/images/exportCSV/prezzo_alle_8.csv'
    installations_link = 'https://www.mise.gov.it/images/exportCSV/anagrafica_impianti_attivi.csv'
    

    response = requests.get(fuel_price_link)
    if response.status_code == 200:
        with open(f'{downloading_folder}fuel_price.csv', 'wb') as file:
                file.write(response.content)

    response = requests.get(installations_link)
    if response.status_code == 200:
        with open(f'{downloading_folder}installations.csv', 'wb') as file:
            file.write(response.content)

def load_db_from_local_files():
    from csv_parser import parse_dict
    from lib.database_handle import execute_insert_dict


    fuel_price_dict = parse_dict(f'{downloading_folder}fuel_price.csv', no_first=1)
    installations_dict = parse_dict(
        f'{downloading_folder}installations.csv', no_first=1)
    
    execute_insert_dict('installations', installations_dict, ('id', 'latitudine', 'longitudine'), ('idImpianto', 'Latitudine', 'Longitudine'))
        
        
         
load_db_from_local_files()

