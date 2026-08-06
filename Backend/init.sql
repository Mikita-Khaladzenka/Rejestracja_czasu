CREATE TABLE pracownicy (
    id INTEGER PRIMARY KEY,
    imie TEXT NOT NULL,
    nazwisko TEXT NOT NULL,
    process TEXT NOT NULL
);

CREATE TABLE czas_pracy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pracownik_id INTEGER NOT NULL,
    data TEXT NOT NULL,
    rozpoczecie TEXT NOT NULL,
    zakonczenie TEXT,
    czas_pracy INTEGER,
    nie_zakonczyl_prace INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (pracownik_id) REFERENCES pracownicy(id)
);
