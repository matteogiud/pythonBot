-- database: d:\giudici matteo\github\pythonBot\py\lib\data\database.db
-- Premi il pulsante ▷ nell'angolo in alto a destra della finestra per eseguire l'intero file.

DROP TABLE IF EXISTS installations;
CREATE TABLE installations (
    id INTEGER PRIMARY KEY NOT NULL,
    nome_impianto TEXT CHECK(length(nome_impianto) <= 255),
    bandiera TEXT CHECK(length(bandiera) <= 255),
    indirizzo TEXT CHECK(length(indirizzo) <= 255),
    comune TEXT CHECK(length(comune) <= 255),
    provincia TEXT CHECK(length(provincia) <= 2),
    latitudine REAL NOT NULL,
    longitudine REAL NOT NULL
);

DROP TABLE IF EXISTS fuel_prices;
CREATE TABLE fuel_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    idImpianto INTEGER NOT NULL REFERENCES installations(id) ON UPDATE CASCADE ON DELETE CASCADE,
    tipoCarburante TEXT CHECK(
        tipoCarburante IN ('BENZINA', 'GASOLIO', 'GPL')
    ) NOT NULL,
    prezzoSelf REAL NOT NULL
);

DROP TABLE IF EXISTS cars;
CREATE TABLE cars (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,    
    tipo_carburante TEXT CHECK(
        tipo_carburante IN ('BENZINA', 'GASOLIO', 'GPL')
    ),
    consumo_km_per_lt REAL,
    capacita_serbatoio INTEGER
);

DROP TABLE IF EXISTS telegram_users;
CREATE TABLE telegram_users (
    chat_id INTEGER PRIMARY KEY NOT NULL,
    username TEXT CHECK(length(username) <= 255),
    car_id INTEGER REFERENCES cars(id) ON UPDATE CASCADE ON DELETE SET NULL    
);