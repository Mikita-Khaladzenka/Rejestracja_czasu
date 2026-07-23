CREATE TABLE pracownicy (
    id INTEGER PRIMARY KEY 
    imie TEXT NOT NULL
  process TEXT NOT NULL DEFAULT '');


CREATE TABLE czas_pracy (
    id INTEGER PRIMARY KEY AUTOINCREMENT 
    pracownik_id INTEGER NOT NULL 
    data DATE NOT NULL 
    rozpoczecie DATETIME NOT NULL 
    zakonczenie DATETIME 
    czas_pracy INTEGER  nie_zakonczyl_prace INTEGER NOT NULL DEFAULT 0 
    FOREIGN KEY (pracownik_id) REFERENCES pracownicy(id)
);


