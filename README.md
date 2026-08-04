# Rejestracja Czasu Pracy

Aplikacja webowa do rejestracji czasu pracy pracowników, oparta na **Flask**, **SQLite** i kodach QR.

System umożliwia:

* rejestrowanie rozpoczęcia i zakończenia pracy,
* identyfikację pracownika za pomocą kodu QR,
* automatyczne obliczanie czasu pracy,
* obsługę języka polskiego i hiszpańskiego,
* zarządzanie pracownikami przez panel administratora,
* generowanie raportów tygodniowych i miesięcznych,
* eksport raportów do formatów PDF i XLSX,
* automatyczne uruchamianie i podtrzymywanie działania aplikacji przez watchdog.

---

# Wymagania

Do uruchomienia aplikacji wymagane są:

* Python 3.10 lub nowszy,
* Flask,
* psutil,
* openpyxl,
* ReportLab,
* SQLite.

Bezpośrednie zależności projektu znajdują się w pliku:

```text
requirements.txt
```

Przykładowa zawartość:

```text
Flask==3.1.2
psutil==7.2.2
openpyxl==3.1.5
reportlab==5.0.0
```

Moduły takie jak `sqlite3`, `datetime`, `pathlib`, `subprocess`, `logging`, `os`, `sys`, `time` i `io` są częścią standardowej biblioteki Pythona i nie wymagają osobnej instalacji.

---

# Instalacja

## 1. Pobranie projektu

Pobierz projekt ręcznie lub sklonuj repozytorium:

```bash
git clone https://github.com/Mikita-Khaladzenka/rejestracja_czasu.git
```

## 2. Przejście do katalogu projektu

```bash
cd rejestracja_czasu
```

Nazwa katalogu może być inna, jeżeli projekt został pobrany jako archiwum ZIP lub zapisany pod inną nazwą.

## 3. Utworzenie środowiska wirtualnego

Środowisko wirtualne oddziela biblioteki projektu od bibliotek zainstalowanych globalnie w systemie.

### Windows

```bat
python -m venv .venv
.venv\Scripts\activate
```

### Linux lub macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4. Instalacja zależności

Po aktywowaniu środowiska wirtualnego wykonaj:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

# Instalacja bez dostępu do internetu

Jeżeli komputer docelowy nie ma dostępu do internetu, pakiety należy wcześniej pobrać na innym komputerze.

Na komputerze z dostępem do internetu wykonaj:

```bash
pip download -r requirements.txt -d packages
```

Polecenie utworzy katalog:

```text
packages/
```

Skopiuj na pendrive:

```text
Rejestracja_czasu/
packages/
```

Na komputerze bez internetu utwórz i aktywuj środowisko wirtualne, a następnie wykonaj:

```bash
pip install --no-index --find-links=packages -r requirements.txt
```

Pakiety powinny być pobierane dla zgodnego systemu operacyjnego, architektury procesora i wersji Pythona.

Najbezpieczniej pobrać je na komputerze z takim samym systemem i taką samą wersją Pythona jak komputer docelowy.

---

# Konfiguracja aplikacji

Przed pierwszym uruchomieniem należy skonfigurować plik:

```text
Backend/config.py
```

Przykładowa konfiguracja:

```python
import os


class Config:

    BASE_DIR = os.path.dirname(
        os.path.abspath(__file__)
    )

    DB = os.path.join(
        BASE_DIR,
        "storage.db"
    )

    FRONTEND = os.path.join(
        BASE_DIR,
        "..",
        "Frontend"
    )

    SECRET_KEY = "Twoj_wlasny_secret_key"

    ADMIN_PASSWORD = "Twoje_haslo_administratora"
```

## Ścieżka do bazy danych

Domyślnie aplikacja korzysta z pliku:

```text
Backend/storage.db
```

Dla domyślnej lokalizacji pozostaw:

```python
DB = os.path.join(
    BASE_DIR,
    "storage.db"
)
```

Takie rozwiązanie wykorzystuje ścieżkę względem katalogu projektu, dzięki czemu aplikację można przenieść na inny komputer lub dysk bez zmiany konfiguracji.

Jeżeli baza znajduje się w innym miejscu, można podać własną ścieżkę.

### Przykład dla Linuxa

```python
DB = "/home/uzytkownik/Rejestracja_czasu/Backend/storage.db"
```

### Przykład dla Windowsa

```python
DB = r"C:\Programy\Rejestracja_czasu\Backend\storage.db"
```

Ścieżka musi wskazywać na tę samą bazę danych, która została utworzona przy użyciu skryptu `init.sql`.

## SECRET_KEY

`SECRET_KEY` jest używany między innymi do zabezpieczania sesji Flask.

Należy zmienić wartość przykładową:

```python
SECRET_KEY = "Twoj_wlasny_secret_key"
```

na własny, trudny do odgadnięcia ciąg znaków, na przykład:

```python
SECRET_KEY = "dlugi_losowy_ciag_znakow_123!@#"
```

Nie należy publikować prawdziwego klucza w publicznym repozytorium.

## Hasło administratora

W polu `ADMIN_PASSWORD` należy ustawić hasło do panelu administratora:

```python
ADMIN_PASSWORD = "Twoje_haslo_administratora"
```

Przykład:

```python
ADMIN_PASSWORD = "MocneHaslo123!"
```

Nie należy pozostawiać domyślnego hasła ani publikować prawdziwego hasła administratora w repozytorium.

---

# Przygotowanie bazy danych

Struktura bazy danych znajduje się w pliku:

```text
Backend/init.sql
```

## Utworzenie bazy przez SQLite CLI

Przejdź do katalogu backendu:

```bash
cd Backend
```

Następnie wykonaj:

```bash
sqlite3 storage.db < init.sql
```

Polecenie utworzy lub zainicjalizuje bazę:

```text
Backend/storage.db
```

Jeżeli baza ma znajdować się w innej lokalizacji, zmień ścieżkę:

```bash
sqlite3 /sciezka/do/bazy/storage.db < init.sql
```

Ścieżka musi być zgodna z wartością `DB` w pliku `Backend/config.py`.

## Sprawdzenie bazy

Otwórz bazę:

```bash
sqlite3 storage.db
```

Wyświetl listę tabel:

```sql
.tables
```

Sprawdź ich strukturę:

```sql
.schema pracownicy
.schema czas_pracy
```

Wyjdź z programu SQLite:

```sql
.quit
```

## Windows bez polecenia `sqlite3`

Jeżeli polecenie `sqlite3` nie jest dostępne, bazę można utworzyć:

* za pomocą programu DB Browser for SQLite,
* za pomocą rozszerzenia SQLite w edytorze,
* przez wykonanie zawartości `init.sql` w narzędziu obsługującym SQLite,
* przez skopiowanie przygotowanego pliku `storage.db` razem z projektem.

---

# Struktura bazy danych

Aplikacja wykorzystuje bazę SQLite.

Domyślna lokalizacja:

```text
Backend/storage.db
```

Baza zawiera dwie główne tabele.

## Tabela `pracownicy`

Przechowuje dane pracowników:

| Pole       | Opis                              |
| ---------- | --------------------------------- |
| `id`       | Unikalny identyfikator pracownika |
| `imie`     | Imię pracownika                   |
| `nazwisko` | Nazwisko pracownika               |
| `process`  | Proces, dział lub miejsce pracy   |

## Tabela `czas_pracy`

Przechowuje historię czasu pracy:

| Pole                  | Opis                                   |
| --------------------- | -------------------------------------- |
| `id`                  | Unikalny identyfikator wpisu           |
| `pracownik_id`        | Identyfikator pracownika               |
| `data`                | Data rozpoczęcia pracy                 |
| `rozpoczecie`         | Data i godzina rozpoczęcia pracy       |
| `zakonczenie`         | Data i godzina zakończenia pracy       |
| `czas_pracy`          | Łączny czas pracy zapisany w sekundach |
| `nie_zakonczyl_prace` | Informacja o niezakończonej zmianie    |

---

# Dodawanie pracowników

Pracowników można dodawać przez panel administratora.

Panel zapisuje:

* identyfikator,
* imię,
* nazwisko,
* proces lub dział.

Można również dodać pracowników ręcznie przez SQL:

```sql
INSERT INTO pracownicy (
    id,
    imie,
    nazwisko,
    process
)
VALUES (
    1,
    'Jan',
    'Kowalski',
    'Logistyka'
);
```

Dodanie kilku pracowników:

```sql
INSERT INTO pracownicy (
    id,
    imie,
    nazwisko,
    process
)
VALUES
    (1, 'Jan', 'Kowalski', 'Logistyka'),
    (2, 'Anna', 'Nowak', 'Produkcja'),
    (3, 'Piotr', 'Wiśniewski', 'Biuro');
```

Wprowadzone dane można sprawdzić poleceniem:

```sql
SELECT *
FROM pracownicy
ORDER BY id;
```

## Powiązanie identyfikatora z kodem QR

Kod QR pracownika musi zawierać jego identyfikator.

Jeżeli kod QR zawiera:

```text
17
```

w tabeli `pracownicy` musi istnieć rekord:

```sql
SELECT *
FROM pracownicy
WHERE id = 17;
```

Bez odpowiadającego rekordu aplikacja wyświetli komunikat o nieznalezieniu pracownika.

---

# Rejestracja czasu pracy

Pierwszy odczyt kodu QR rozpoczyna sesję pracy.

Przykład:

```text
Rozpoczęcie pracy: 08:10
```

Kolejne odczyty tego samego kodu w ciągu 14 godzin aktualizują godzinę zakończenia tej samej sesji.

Przykład:

```text
08:10 – rozpoczęcie pracy
12:00 – zakończenie ustawione na 12:00
16:01 – zakończenie zaktualizowane na 16:01
```

W takim przypadku nie powstaje nowy rekord przy każdym skanowaniu. Aktualizowany jest istniejący wpis czasu pracy.

Nowa sesja może zostać rozpoczęta po przekroczeniu dopuszczalnego czasu poprzedniej zmiany.

Aplikacja oblicza czas pracy na podstawie różnicy pomiędzy:

```text
rozpoczecie
```

i:

```text
zakonczenie
```

---

# Obsługa języków

Strona rejestracji obsługuje dwa języki:

* polski,
* hiszpański.

Wybrany język jest zapisywany w `localStorage` przeglądarki.

Komunikaty obejmują między innymi:

* rozpoczęcie pracy,
* zakończenie pracy,
* brak identyfikatora,
* błędny kod QR,
* nieznalezionego pracownika,
* błąd połączenia z serwerem,
* błąd uruchamiania kamery.

---

# Uruchomienie ręczne

Z katalogu głównego projektu wykonaj:

```bash
python Backend/app.py
```

Na niektórych systemach:

```bash
python3 Backend/app.py
```

Można również przejść wcześniej do katalogu backendu:

```bash
cd Backend
python app.py
```

Po uruchomieniu aplikacja powinna być dostępna pod adresami:

```text
http://127.0.0.1:5000
```

oraz:

```text
http://localhost:5000
```

Jeżeli Flask nasłuchuje na wszystkich interfejsach sieciowych, terminal może również wyświetlić adres lokalny, na przykład:

```text
http://192.168.1.102:5000
```

---

# Uruchamianie w tle na Windows

Projekt zawiera plik:

```text
Rejestracja Czasu Pracy.bat
```

Plik powinien znajdować się w katalogu głównym projektu obok `.venv` i katalogu `Backend`.

Przykładowa zawartość:

```bat
@echo off

set "PROJECT_DIR=%~dp0"
set "PYTHONW=%PROJECT_DIR%.venv\Scripts\pythonw.exe"
set "WATCHDOG=%PROJECT_DIR%Backend\watchdog.py"

if not exist "%PYTHONW%" (
    echo Nie znaleziono interpretera:
    echo %PYTHONW%
    pause
    exit /b 1
)

if not exist "%WATCHDOG%" (
    echo Nie znaleziono pliku:
    echo %WATCHDOG%
    pause
    exit /b 1
)

start "" /D "%PROJECT_DIR%Backend" "%PYTHONW%" "%WATCHDOG%"

exit /b 0
```

Zmienne są budowane na podstawie lokalizacji pliku `.bat`, dlatego nie trzeba wpisywać bezwzględnej ścieżki do projektu.

Po dwukrotnym kliknięciu pliku:

1. uruchamiany jest `Backend/watchdog.py`,
2. watchdog uruchamia `Backend/app.py`,
3. procesy działają bez otwartego okna konsoli,
4. watchdog sprawdza, czy aplikacja nadal działa,
5. jeżeli aplikacja zostanie zakończona, watchdog uruchamia ją ponownie.

---

# Watchdog

Plik:

```text
Backend/watchdog.py
```

odpowiada za monitorowanie procesu aplikacji.

Watchdog:

* korzysta ze ścieżek lokalnych względem projektu,
* nie wymaga wpisywania pełnej ścieżki użytkownika,
* używa interpretera z aktywnego środowiska `.venv`,
* na Windows korzysta z `pythonw.exe`,
* uruchamia aplikację bez okna konsoli,
* na Linuxie uruchamia proces w osobnej sesji,
* zapisuje informacje do pliku:

```text
Backend/watchdog.log
```

Log może zawierać między innymi:

* informację o uruchomieniu watchdoga,
* informację o uruchomieniu `app.py`,
* błędy procesu monitorującego.

## Ważne

Wielokrotne uruchomienie pliku `.bat` może spowodować działanie kilku procesów watchdoga jednocześnie.

Przed ponownym uruchomieniem warto sprawdzić Menedżer zadań i zakończyć wcześniejsze procesy `pythonw.exe`, jeżeli nie są już potrzebne.

---

# Panel administratora

Panel administratora znajduje się pod adresem:

```text
http://127.0.0.1:5000/adm
```

lub:

```text
http://localhost:5000/adm
```

Do logowania należy użyć hasła ustawionego w:

```text
Backend/config.py
```

w polu:

```python
ADMIN_PASSWORD
```

Panel umożliwia:

* logowanie administratora,
* wyświetlanie listy pracowników,
* dodawanie pracowników,
* usuwanie pracowników,
* wybór typu raportu,
* wybór roku,
* wybór miesiąca lub tygodnia,
* wybór formatu PDF lub XLSX,
* generowanie i pobieranie raportów.

---

# Raporty

Aplikacja umożliwia generowanie raportów:

* tygodniowych,
* miesięcznych.

Obsługiwane formaty:

* PDF,
* XLSX.

## Raport tygodniowy

Raport tygodniowy zawiera siedem dni wybranego tygodnia.

Dla każdego dnia dostępne są kolumny:

```text
R – rozpoczęcie pracy
K – zakończenie pracy
```

## Raport miesięczny

Raport miesięczny zawiera wszystkie dni wybranego miesiąca w jednym poziomym układzie.

Przykładowy układ:

```text
Imię | Nazwisko | 01.08 | 02.08 | 03.08 | ... | Suma
```

Raport PDF wykorzystuje niestandardową szerokość strony, aby wszystkie dni miesiąca znajdowały się w jednym wierszu.

W przeglądarce PDF raport można:

* powiększać,
* pomniejszać,
* przesuwać poziomo,
* drukować po odpowiednim dopasowaniu skali.

## Nazwy plików raportów

Nazwa pliku uwzględnia:

* typ raportu,
* wybrany okres,
* rok,
* datę wygenerowania,
* format pliku.

Przykład raportu tygodniowego:

```text
Raport za tydzień 32 2026 wygenerowany 04-08-2026.xlsx
```

Przykład raportu miesięcznego:

```text
Raport za sierpień 2026 wygenerowany 04-08-2026.pdf
```

---

# Polskie znaki w raportach PDF

ReportLab nie zapewnia pełnej obsługi polskich znaków przy użyciu każdej domyślnej czcionki.

Dlatego projekt zawiera lokalne pliki:

```text
Backend/assets/fonts/DejaVuSans.ttf
Backend/assets/fonts/DejaVuSans-Bold.ttf
```

Czcionki są rejestrowane przez:

```text
Backend/raport/pdf_generator.py
```

Ścieżka do nich jest obliczana względem lokalizacji projektu, dzięki czemu raporty działają po przeniesieniu aplikacji na inny komputer.

Do działania raportów PDF wymagane są oba pliki:

```text
DejaVuSans.ttf
DejaVuSans-Bold.ttf
```

Nie należy ich usuwać ani zmieniać ich nazw.

---

# Kamera i kody QR

Aplikację należy otwierać przez serwer Flask:

```text
http://localhost:5000
```

lub:

```text
http://127.0.0.1:5000
```

Nie należy otwierać pliku `Frontend/index.html` bezpośrednio z dysku.

## Dostęp przez adres IP

Przy otwarciu aplikacji przez lokalny adres IP, na przykład:

```text
http://192.168.1.102:5000
```

przeglądarka może uznać połączenie za niezabezpieczone i zablokować dostęp do kamery.

Dostęp do kamery poza `localhost` może wymagać połączenia HTTPS.

## Typowe problemy z odczytem kodu QR

Na skuteczność odczytu wpływają:

* oświetlenie,
* ostrość kamery,
* wielkość kodu,
* odległość od kamery,
* odbicia światła na ekranie telefonu,
* zabrudzenie obiektywu,
* brak uprawnień do kamery,
* używanie kamery przez inną aplikację.

---

# Struktura projektu

```text
Rejestracja_czasu/
│
├── README.md
├── Struct.md
├── requirements.txt
├── Rejestracja Czasu Pracy.bat
│
├── Backend/
│   ├── app.py
│   ├── config.py
│   ├── init.sql
│   ├── storage.db
│   ├── watchdog.py
│   │
│   ├── assets/
│   │   └── fonts/
│   │       ├── DejaVuSans.ttf
│   │       └── DejaVuSans-Bold.ttf
│   │
│   ├── controllers/
│   │   ├── admin_controller.py
│   │   ├── frontend_controller.py
│   │   ├── registration_controller.py
│   │   └── report_controller.py
│   │
│   ├── database/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── employee.py
│   │   └── worktime.py
│   │
│   ├── raport/
│   │   ├── excel_generator.py
│   │   ├── pdf_generator.py
│   │   ├── report_data_builder.py
│   │   ├── report_date_range.py
│   │   ├── report_filename.py
│   │   └── report_table_builder.py
│   │
│   ├── repositories/
│   │   ├── employee_repository.py
│   │   ├── report_repository.py
│   │   └── worktime_repository.py
│   │
│   └── services/
│       ├── admin_service.py
│       ├── registration_service.py
│       └── report_service.py
│
└── Frontend/
    ├── index.html
    ├── script.js
    ├── style.css
    ├── adm.html
    ├── adm.js
    └── adm.css
```

Szczegółowy opis plików znajduje się w:

```text
Struct.md
```

---

# Architektura aplikacji

Projekt został podzielony na warstwy:

```text
Frontend
    |
    v
Controller
    |
    v
Service
    |
    v
Repository
    |
    v
Database
```

## Frontend

Odpowiada za:

* interfejs użytkownika,
* obsługę kamery,
* skanowanie kodów QR,
* obsługę panelu administratora,
* wybór parametrów raportów,
* komunikację z backendem.

## Controller

Odpowiada za:

* obsługę żądań HTTP,
* odczytywanie danych wejściowych,
* wywoływanie odpowiednich serwisów,
* zwracanie odpowiedzi JSON lub plików.

## Service

Odpowiada za:

* logikę biznesową,
* obsługę rozpoczęcia i zakończenia pracy,
* zarządzanie pracownikami,
* koordynację generowania raportów.

## Repository

Odpowiada za:

* wykonywanie zapytań SQL,
* odczytywanie danych,
* dodawanie i usuwanie pracowników,
* tworzenie i aktualizowanie wpisów czasu pracy,
* pobieranie danych raportowych.

## Model

Odpowiada za reprezentowanie danych aplikacji jako obiektów.

## Database

Odpowiada za tworzenie połączeń z bazą SQLite.

---

# Technologie

Projekt wykorzystuje:

* Python,
* Flask,
* SQLite,
* psutil,
* openpyxl,
* ReportLab,
* HTML5,
* CSS3,
* JavaScript,
* bibliotekę do odczytywania kodów QR w przeglądarce,
* czcionki DejaVu Sans.

---

# Kolejność pierwszego uruchomienia

Przed pierwszym uruchomieniem należy:

1. Pobrać lub skopiować projekt.
2. Utworzyć środowisko wirtualne `.venv`.
3. Aktywować środowisko.
4. Zainstalować zależności z `requirements.txt`.
5. Ustawić `SECRET_KEY` w `Backend/config.py`.
6. Ustawić `ADMIN_PASSWORD` w `Backend/config.py`.
7. Sprawdzić ścieżkę `DB`.
8. Utworzyć bazę za pomocą `Backend/init.sql`.
9. Sprawdzić obecność czcionek w `Backend/assets/fonts`.
10. Uruchomić aplikację.
11. Otworzyć `http://localhost:5000`.
12. Zalogować się do panelu administratora.
13. Dodać pracowników.
14. Przygotować kody QR zawierające ich identyfikatory.
15. Przetestować rozpoczęcie i zakończenie pracy.
16. Przetestować raport tygodniowy i miesięczny.
17. Na Windowsie przetestować uruchomienie przez plik `.bat`.

Bez utworzonej bazy i danych w tabeli `pracownicy` rejestracja czasu pracy nie będzie działała poprawnie.

---

# Testowe polecenia SQL

## Wyświetlenie pracowników

```sql
SELECT *
FROM pracownicy
ORDER BY id;
```

## Wyświetlenie historii czasu pracy

```sql
SELECT *
FROM czas_pracy
ORDER BY id;
```

## Dodanie przykładowego wpisu

```sql
INSERT INTO czas_pracy (
    pracownik_id,
    data,
    rozpoczecie,
    zakonczenie,
    czas_pracy
)
VALUES (
    1,
    '2026-08-04',
    '2026-08-04 08:10:00',
    '2026-08-04 16:01:00',
    28260
);
```

Wartość `28260` oznacza 7 godzin i 51 minut.

## Usunięcie wpisu testowego

```sql
DELETE FROM czas_pracy
WHERE id = 24;
```

---

# Bezpieczeństwo

W środowisku produkcyjnym należy:

* używać silnego hasła administratora,
* używać losowego `SECRET_KEY`,
* nie publikować pliku `config.py` z prawdziwymi danymi,
* ograniczyć dostęp do panelu administratora,
* wykonywać kopie zapasowe `storage.db`,
* zabezpieczyć komputer uruchamiający aplikację,
* rozważyć HTTPS przy dostępie przez sieć,
* nie udostępniać pliku bazy nieuprawnionym osobom.

---

# Kopia zapasowa

Cała historia czasu pracy znajduje się w:

```text
Backend/storage.db
```

Aby wykonać kopię zapasową, zatrzymaj aplikację i skopiuj plik w bezpieczne miejsce.

Nie zaleca się synchronizowania aktywnie używanego pliku SQLite bezpośrednio przez OneDrive lub podobne usługi, ponieważ jednoczesna synchronizacja i zapis mogą doprowadzić do konfliktu lub uszkodzenia bazy.

Bezpieczniej kopiować bazę po zamknięciu aplikacji albo wykonywać okresowe kopie zapasowe.
