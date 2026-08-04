```text
Rejestracja_czasu/
│
<<<<<<< HEAD
├── README.md
│   // Instrukcja instalacji, konfiguracji i uruchomienia aplikacji.
│
├── Struct.md
│   // Opis struktury katalogów i odpowiedzialności poszczególnych plików.
│
├── requirements.txt
│   // Lista bibliotek Pythona wymaganych do działania aplikacji.
│
├── Rejestracja Czasu Pracy.bat
│   // Skrypt uruchamiający watchdog.py w tle na systemie Windows.
│
├── Backend/
│   │
│   ├── app.py
│   │   // Główny plik uruchamiający aplikację Flask.
│   │   // Tworzy aplikację, wczytuje konfigurację i rejestruje kontrolery.
│   │
│   ├── config.py
│   │   // Konfiguracja aplikacji, między innymi ścieżki,
│   │   // SECRET_KEY oraz hasło administratora.
│   │
│   ├── init.sql
│   │   // Skrypt SQL tworzący strukturę bazy danych.
│   │
│   ├── storage.db
│   │   // Baza danych SQLite przechowująca dane aplikacji.
│   │   │
│   │   ├── czas_pracy
│   │   │   // Tabela przechowująca historię rejestracji czasu pracy.
│   │   │   │
│   │   │   ├── id
│   │   │   │   // Unikalny identyfikator wpisu.
│   │   │   │
│   │   │   ├── pracownik_id
│   │   │   │   // Identyfikator pracownika powiązanego z wpisem.
│   │   │   │
│   │   │   ├── data
│   │   │   │   // Data rozpoczęcia pracy.
│   │   │   │
│   │   │   ├── rozpoczecie
│   │   │   │   // Data i godzina rozpoczęcia pracy.
│   │   │   │
│   │   │   ├── zakonczenie
│   │   │   │   // Data i godzina zakończenia pracy.
│   │   │   │
│   │   │   ├── czas_pracy
│   │   │   │   // Łączny czas pracy zapisany w sekundach.
│   │   │   │
│   │   │   └── nie_zakonczyl_prace
│   │   │       // Flaga informująca o niezamkniętej zmianie.
│   │   │
│   │   └── pracownicy
│   │       // Tabela przechowująca dane pracowników.
│   │       │
│   │       ├── id
│   │       │   // Unikalny identyfikator pracownika.
│   │       │
│   │       ├── imie
│   │       │   // Imię pracownika.
│   │       │
│   │       ├── nazwisko
│   │       │   // Nazwisko pracownika.
│   │       │
│   │       └── process
│   │           // Nazwa procesu, działu lub stanowiska pracownika.
│   │
│   ├── watchdog.py
│   │   // Monitoruje działanie app.py i ponownie uruchamia aplikację,
│   │   // jeżeli jej proces zostanie zakończony.
│   │   // Używa lokalnych ścieżek projektu i na Windows uruchamia
│   │   // aplikację przez pythonw.exe w tle.
│   │
│   ├── assets/
│   │   └── fonts/
│   │       ├── DejaVuSans.ttf
│   │       │   // Czcionka Unicode używana w raportach PDF.
│   │       │   // Obsługuje polskie znaki.
│   │       │
│   │       └── DejaVuSans-Bold.ttf
│   │           // Pogrubiona wersja czcionki używana w nagłówkach PDF.
│   │
│   ├── controllers/
│   │   ├── admin_controller.py
│   │   │   // Obsługuje żądania HTTP panelu administratora.
│   │   │   // Odpowiada za logowanie, dodawanie i usuwanie pracowników
│   │   │   // oraz generowanie raportów z panelu administratora.
│   │   │
│   │   ├── frontend_controller.py
│   │   │   // Udostępnia pliki HTML, CSS i JavaScript użytkownikowi.
│   │   │
│   │   ├── registration_controller.py
│   │   │   // Obsługuje żądania dotyczące rejestracji
│   │   │   // rozpoczęcia i zakończenia pracy.
│   │   │
│   │   └── report_controller.py
│   │       // Obsługuje żądania HTTP związane z generowaniem raportów.
│   │
│   ├── database/
│   │   └── database.py
│   │       // Tworzy i konfiguruje połączenie z bazą danych SQLite.
│   │
│   ├── models/
│   │   ├── employee.py
│   │   │   // Model reprezentujący pracownika.
│   │   │
│   │   └── worktime.py
│   │       // Model reprezentujący wpis czasu pracy.
│   │
│   ├── raport/
│   │   ├── excel_generator.py
│   │   │   // Generuje raporty w formacie XLSX.
│   │   │
│   │   ├── pdf_generator.py
│   │   │   // Generuje raporty w formacie PDF.
│   │   │   // Obsługuje polskie znaki i szeroki układ raportu miesięcznego.
│   │   │
│   │   ├── report_data_builder.py
│   │   │   // Pobiera i przygotowuje dane potrzebne do utworzenia raportu.
│   │   │
│   │   ├── report_date_range.py
│   │   │   // Wyznacza zakres dat dla raportu tygodniowego
│   │   │   // lub miesięcznego.
│   │   │
│   │   ├── report_filename.py
│   │   │   // Buduje nazwę pliku raportu na podstawie typu,
│   │   │   // wybranego okresu i daty wygenerowania.
│   │   │
│   │   └── report_table_builder.py
│   │       // Buduje wspólną strukturę tabeli wykorzystywaną
│   │       // przez generatory raportów PDF i XLSX.
│   │
│   ├── repositories/
│   │   ├── employee_repository.py
│   │   │   // Wykonuje operacje SQL na tabeli pracownicy.
│   │   │   // Odpowiada za wyszukiwanie, dodawanie i usuwanie pracowników.
│   │   │
│   │   ├── report_repository.py
│   │   │   // Pobiera z bazy dane wymagane do generowania raportów.
│   │   │
│   │   └── worktime_repository.py
│   │       // Wykonuje operacje SQL na tabeli czas_pracy.
│   │       // Odpowiada za tworzenie i aktualizowanie sesji pracy.
│   │
│   └── services/
│       ├── admin_service.py
│       │   // Zawiera logikę biznesową panelu administratora.
│       │   // Obsługuje logowanie oraz zarządzanie pracownikami.
│       │
│       ├── registration_service.py
│       │   // Zawiera logikę rejestracji czasu pracy.
│       │   // Pierwszy odczyt QR rozpoczyna sesję, a kolejne odczyty
│       │   // w ciągu 14 godzin aktualizują godzinę zakończenia.
│       │
│       └── report_service.py
│           // Fasada modułu raportów.
│           // Koordynuje zakres dat, dane, budowę tabeli,
│           // nazwę pliku i generowanie raportu.
│
└── Frontend/
    ├── index.html
    │   // Główna strona aplikacji służąca do rejestracji
    │   // rozpoczęcia i zakończenia pracy za pomocą kodu QR.
    │
    ├── script.js
    │   // Obsługuje kamerę, skanowanie kodów QR,
    │   // komunikację z backendem oraz język polski i hiszpański.
    │
    ├── style.css
    │   // Arkusz stylów głównej strony aplikacji.
    │
    ├── adm.html
    │   // Strona panelu administratora.
    │
    ├── adm.js
    │   // Obsługuje logowanie administratora, zarządzanie pracownikami,
    │   // wybór parametrów raportu i pobieranie wygenerowanych plików.
    │
    └── adm.css
        // Arkusz stylów panelu administratora.
```
=======
├── Backend/
│   ├── app.py                     // Główny plik uruchamiający aplikację Flask. Tworzy aplikację, wczytuje konfigurację i rejestruje kontrolery.
│   ├── config.py                  // Plik konfiguracyjny zawierający ustawienia aplikacji (ścieżki, SECRET_KEY, hasło administratora).
│   ├── init.sql                   // Skrypt SQL tworzący strukturę bazy danych.
│   ├── storage.db                 // Baza danych SQLite przechowująca dane aplikacji.
│   │   ├── czas_pracy             // Tabela przechowująca historię rejestracji czasu pracy.
│   │   │   ├── id                 // Unikalny identyfikator wpisu.
│   │   │   ├── pracownik_id       // Identyfikator pracownika powiązanego z wpisem.
│   │   │   ├── data               // Data rozpoczęcia zmiany.
│   │   │   ├── rozpoczecie        // Data i godzina rozpoczęcia pracy.
│   │   │   ├── zakonczenie        // Data i godzina zakończenia pracy.
│   │   │   ├── czas_pracy         // Łączny czas pracy zapisany w sekundach.
│   │   │   └── nie_zakonczyl_prace// Flaga informująca o niezamkniętej zmianie.
│   │   │
│   │   └── pracownicy            // Tabela przechowująca dane pracowników.
│   │       ├── id                // Unikalny identyfikator pracownika.
│   │       ├── imie              // Imię pracownika.
│   │       └── process           // Nazwa procesu lub działu pracownika.
│   │
│   ├── controllers/
│   │   ├── admin_controller.py       // Obsługuje żądania HTTP związane z panelem administratora.
│   │   ├── frontend_controller.py    // Udostępnia pliki HTML, CSS i JavaScript użytkownikowi.
│   │   └── registration_controller.py// Obsługuje żądania dotyczące rejestracji czasu pracy.
│   │
│   ├── database/
│   │   └── database.py           // Tworzy i konfiguruje połączenie z bazą SQLite.
│   │
│   ├── models/
│   │   ├── employee.py           // Model reprezentujący obiekt pracownika.
│   │   └── worktime.py           // Model reprezentujący wpis czasu pracy.
│   │
│   ├── repositories/
│   │   ├── employee_repository.py    // Wykonuje operacje SQL na tabeli pracownicy.
│   │   └── worktime_repository.py    // Wykonuje operacje SQL na tabeli czas_pracy.
│   │
│   └── services/
│       ├── admin_service.py          // Zawiera logikę biznesową panelu administratora.
│       └── registration_service.py   // Zawiera logikę biznesową rejestracji czasu pracy.
│
└── Frontend/
    ├── index.html                // Główna strona aplikacji służąca do rejestracji wejść i wyjść.
    ├── script.js                 // Obsługuje logikę strony głównej oraz komunikację z backendem.
    ├── style.css                 // Arkusz stylów strony głównej.
    ├── adm.html                  // Strona panelu administratora.
    ├── adm.js                    // Obsługuje logikę panelu administratora oraz komunikację z backendem.
    └── adm.css                   // Arkusz stylów panelu administratora.
```
>>>>>>> 35a7e7fb6b192a5b71ce7e4aab5652b9d0980974
