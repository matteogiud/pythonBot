from ...data.dinamic.database_handle import *
from .telegram_users import *


class DbGasStation:
    def __init__(self, latitudine, longitudine, nome_impianto=None, bandiera=None, indirizzo=None, comune=None, provincia=None, distance=None):
        self.latitudine = latitudine
        self.longitudine = longitudine
        self.nome_impianto = nome_impianto
        self.bandiera = bandiera
        self.indirizzo = indirizzo
        self.comune = comune
        self.provincia = provincia
        self.distance = distance

    @staticmethod
    def get_closer_gas_stations(latitudine, longitudine) -> list:
        stations = get_closer_gas_station_from_db(latitudine, longitudine)

        return [DbGasStation(station['latitudine'], station['longitudine'], station['nome_impianto'], station['bandiera'], station['indirizzo'], station['comune'], station['provincia'], station['distance']) for station in stations]

    @staticmethod
    def get_cheaper_gas_stations(latitudine, longitudine, liters, user: DbTelgramUser):
        pass # TODO
    
