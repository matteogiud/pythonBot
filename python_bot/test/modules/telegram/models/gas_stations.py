from ...data.dinamic.database_handle import (
    get_cheaper_gas_station_from_db,
    get_closer_gas_station_from_db,
)
from .telegram_users import *


class DbGasStation:
    def __init__(
        self,
        latitudine,
        longitudine,
        nome_impianto=None,
        bandiera=None,
        indirizzo=None,
        comune=None,
        provincia=None,
        distance=None,
        selfPrice=None,
    ):
        self.latitudine = latitudine
        self.longitudine = longitudine
        self.nome_impianto = nome_impianto
        self.bandiera = bandiera
        self.indirizzo = indirizzo
        self.comune = comune
        self.provincia = provincia
        self.distance = distance
        self.selfPrice = selfPrice

    @staticmethod
    def get_closer_gas_stations(latitudine, longitudine, user: DbTelgramUser, limit=5) -> list:
        stations = get_closer_gas_station_from_db(latitudine, longitudine, user, limit=limit)

        return [
            DbGasStation(
                station["latitudine"],
                station["longitudine"],
                station["nome_impianto"],
                station["bandiera"],
                station["indirizzo"],
                station["comune"],
                station["provincia"],
                station["distance"],
                station["prezzoSelf"],
            )
            for station in stations
        ]

    @staticmethod
    def get_cheaper_gas_stations(
        latitudine, longitudine, liters, user: DbTelgramUser, limit=5
    ) -> list:
        closer_stations = get_cheaper_gas_station_from_db(
            latitudine, longitudine, user, liters, limit=limit
        )
        return [
            DbGasStation(
                station["latitudine"],
                station["longitudine"],
                station["nome_impianto"],
                station["bandiera"],
                station["indirizzo"],
                station["comune"],
                station["provincia"],
                station["distance"],
                station["prezzoSelf"],
            )
            for station in closer_stations
        ]
