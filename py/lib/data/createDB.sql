-- database: d:\giudici matteo\github\pythonBot\py\lib\data\database.db

-- Premi il pulsante ▷ nell'angolo in alto a destra della finestra per eseguire l'intero file.

DROP TABLE fuel_prices;

CREATE TABLE installations (id INTEGER PRIMARY KEY NOT NULL, nome_impianto TEXT CHECK( length(nome_impianto) <= 255 ), bandiera TEXT CHECK( length(bandiera) <= 255 ), indirizzo TEXT CHECK( length(indirizzo) <= 255 ), comune TEXT CHECK( length(comune) <=255 ), provincia TEXT CHECK( length(provincia) <=2 ), latitudine REAL NOT NULL, longitudine REAL NOT NULL);



CREATE TABLE fuel_prices (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, idImpianto INTEGER NOT NULL REFERENCES installations(id) ON UPDATE CASCADE ON DELETE CASCADE, tipoCarburante TEXT CHECK( tipoCarburante IN ('BENZINA', 'GASOLIO', 'GPL') ) NOT NULL, prezzoSelf REAL NOT NULL);