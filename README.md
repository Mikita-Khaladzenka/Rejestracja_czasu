# Rejestracja Czasu Pracy

Prosta aplikacja do rejestracji czasu pracy oparta na **Flask** oraz **SQLite**.

System umożliwia:

* rejestrację rozpoczęcia i zakończenia pracy,
* identyfikację pracownika za pomocą kodu QR,
* kontrolę czasu pracy,
* zarządzanie pracownikami przez panel administratora.

---

# Wymagania

Do uruchomienia aplikacji wymagane są:

* Python 3.10 lub nowszy,
* Flask,
* SQLite.

---

# Instalacja

## 1. Pobranie projektu

Pobierz projekt lub sklonuj repozytorium:

```bash
git clone <https://github.com/Mikita-Khaladzenka/rejestracja_czasu.git>
```

## 2. Przejście do katalogu projektu

```bash
cd Rejestracja_czasu
```

## 3. Utworzenie środowiska wirtualnego

Utworzenie środowiska wirtualnego jest zalecane, ponieważ pozwala oddzielić biblioteki projektu od bibliotek zainstalowanych globalnie w systemie.

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4. Instalacja zależności

W katalogu głównym projektu znajduje się plik:

```text
requirements.txt
```

Zainstaluj wszystkie wymagane biblioteki:

```bash
pip install -r requirements.txt
```

---

# Konfiguracja aplikacji

Przed pierwszym uruchomieniem aplikacji należy skonfigurować plik:

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

W polu `DB` należy wpisać prawidłową ścieżkę do pliku bazy danych SQLite.

Domyślnie aplikacja korzysta z pliku:

```text
Backend/storage.db
```

Plik bazy danych należy utworzyć przed pierwszym uruchomieniem aplikacji.

Dla domyślnej lokalizacji można pozostawić:

```python
DB = os.path.join(
    BASE_DIR,
    "storage.db"
)
```

Jeżeli baza danych znajduje się w innym miejscu, należy podać własną ścieżkę, na przykład:

```python
DB = "/home/uzytkownik/Rejestracja_czasu/Backend/storage.db"
```

W systemie Windows można użyć:

```python
DB = r"C:\Users\Uzytkownik\Rejestracja_czasu\Backend\storage.db"
```

Ścieżka musi wskazywać na tę samą bazę danych, która została utworzona przy użyciu skryptu `init.sql`.

## SECRET_KEY

Wartość `SECRET_KEY` służy między innymi do zabezpieczania sesji Flask.

Należy zmienić wartość przykładową:

```python
SECRET_KEY = "Twoj_wlasny_secret_key"
```

na własny, trudny do odgadnięcia ciąg znaków.

Przykład:

```python
SECRET_KEY = "dlugi_losowy_ciag_znakow_123!@#"
```

Nie należy publikować prawdziwego klucza `SECRET_KEY` w publicznym repozytorium.

## Hasło administratora

W polu `ADMIN_PASSWORD` należy ustawić własne hasło do panelu administratora:

```python
ADMIN_PASSWORD = "Twoje_haslo_administratora"
```

Przykład:

```python
ADMIN_PASSWORD = "MocneHaslo123!"
```

Nie należy pozostawiać domyślnego hasła ani publikować prawdziwego hasła administratora w publicznym repozytorium.

---

# Przygotowanie bazy danych

Przed uruchomieniem aplikacji należy utworzyć strukturę bazy danych za pomocą skryptu:

```text
Backend/init.sql
```

## 1. Przejście do katalogu backendu

```bash
cd Backend
```

## 2. Utworzenie bazy danych

Uruchom skrypt `init.sql` dla wybranego pliku bazy danych:

```bash
sqlite3 storage.db < init.sql
```

Polecenie utworzy plik bazy danych oraz wymagane tabele:

```text
Backend/storage.db
```

Jeżeli używana jest inna nazwa lub ścieżka bazy danych, należy odpowiednio zmienić polecenie:

```bash
sqlite3 /sciezka/do/bazy/storage.db < init.sql
```

Ścieżka użyta podczas tworzenia bazy danych musi być zgodna z wartością `DB` ustawioną w pliku `config.py`.

## 3. Sprawdzenie utworzonych tabel

Bazę danych można otworzyć poleceniem:

```bash
sqlite3 storage.db
```

Następnie można wyświetlić listę tabel:

```sql
.tables
```

Można również sprawdzić strukturę tabel:

```sql
.schema pracownicy
.schema czas_pracy
```

Aby wyjść z SQLite:

```sql
.quit
```

---

# Dodawanie danych pracowników

Po utworzeniu tabel należy dodać dane pracowników do tabeli:

```text
pracownicy
```

Przykładowe polecenie:

```sql
INSERT INTO pracownicy (id, imie, process)
VALUES (1, 'Jan Kowalski', 'Logistyka');
```

Można również dodać wielu pracowników jednym poleceniem:

```sql
INSERT INTO pracownicy (id, imie, process) VALUES
(1, 'Jan Kowalski', 'Logistyka'),
(2, 'Anna Nowak', 'Produkcja'),
(3, 'Piotr Wiśniewski', 'Biuro');
```

Dane można wprowadzić bezpośrednio w terminalu SQLite:

```bash
sqlite3 storage.db
```

Następnie należy wykonać polecenie SQL:

```sql
INSERT INTO pracownicy (id, imie, process) VALUES
(1, 'Jan Kowalski', 'Logistyka'),
(2, 'Anna Nowak', 'Produkcja');
```

Wprowadzone dane można sprawdzić poleceniem:

```sql
SELECT * FROM pracownicy ORDER BY id;
```

## Ważne

Bez danych w tabeli `pracownicy` system nie będzie w stanie rozpoznać pracownika na podstawie kodu QR.

W konsekwencji aplikacja nie będzie mogła:

* przypisać rozpoczęcia pracy do konkretnego pracownika,
* przypisać zakończenia pracy,
* obliczyć czasu pracy,
* zapisać poprawnego wpisu w tabeli `czas_pracy`.

Identyfikator zapisany w kodzie QR musi odpowiadać wartości `id` istniejącej w tabeli `pracownicy`.

Przykład:

Jeżeli kod QR zawiera:

```text
17
```

w tabeli `pracownicy` musi istnieć rekord z identyfikatorem `17`.

Można to sprawdzić poleceniem:

```sql
SELECT * FROM pracownicy WHERE id = 17;
```

---

# Uruchomienie aplikacji

Przejdź do katalogu backendu:

```bash
cd Backend
```

Uruchom serwer Flask:

```bash
python app.py
```

W niektórych systemach należy użyć:

```bash
python3 app.py
```

Po uruchomieniu aplikacja będzie dostępna pod adresem:

```text
http://127.0.0.1:5000
```

lub:

```text
http://localhost:5000
```

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

Do logowania należy użyć hasła ustawionego w pliku:

```text
Backend/config.py
```

w polu:

```python
ADMIN_PASSWORD
```

Panel umożliwia:

* logowanie administratora,
* dodawanie pracowników,
* usuwanie pracowników,
* przeglądanie listy pracowników.

---

# Struktura projektu

```text
Rejestracja_czasu/
│
├── Backend/
│   ├── app.py
│   ├── config.py
│   ├── init.sql
│   ├── storage.db
│   │
│   ├── controllers/
│   │   ├── admin_controller.py
│   │   ├── frontend_controller.py
│   │   └── registration_controller.py
│   │
│   ├── database/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── employee.py
│   │   └── worktime.py
│   │
│   ├── repositories/
│   │   ├── employee_repository.py
│   │   └── worktime_repository.py
│   │
│   └── services/
│       ├── admin_service.py
│       └── registration_service.py
│
└── Frontend/
    ├── index.html
    ├── script.js
    ├── style.css
    ├── adm.html
    ├── adm.js
    └── adm.css
```

---

# Baza danych

Aplikacja wykorzystuje bazę SQLite.

Domyślna lokalizacja bazy:

```text
Backend/storage.db
```

Rzeczywista lokalizacja bazy zależy od wartości `DB` ustawionej w pliku:

```text
Backend/config.py
```

Baza zawiera dwie główne tabele.

## Tabela `pracownicy`

Przechowuje dane pracowników:

| Pole      | Opis                            |
| --------- | ------------------------------- |
| `id`      | Identyfikator pracownika        |
| `imie`    | Imię pracownika                 |
| `process` | Proces, dział lub miejsce pracy |

## Tabela `czas_pracy`

Przechowuje historię czasu pracy:

| Pole                  | Opis                                |
| --------------------- | ----------------------------------- |
| `id`                  | Identyfikator wpisu                 |
| `pracownik_id`        | Identyfikator pracownika            |
| `data`                | Data pracy                          |
| `rozpoczecie`         | Czas rozpoczęcia pracy              |
| `zakonczenie`         | Czas zakończenia pracy              |
| `czas_pracy`          | Czas pracy w sekundach              |
| `nie_zakonczyl_prace` | Informacja o niezakończonej zmianie |

---

# Ważna uwaga dotycząca kamery i kodów QR

Aplikację należy uruchamiać przez serwer Flask:

```text
http://localhost:5000
```

lub:

```text
http://127.0.0.1:5000
```

Nie należy korzystać ze zwykłego połączenia HTTP przez lokalny adres IP komputera, na przykład:

```text
http://192.168.x.x:5000
```

Przeglądarka może uznać takie połączenie za niezabezpieczone i zablokować dostęp do kamery.

Do działania kamery poza `localhost` może być wymagane połączenie HTTPS.

---

# Kolejność pierwszego uruchomienia

Przed pierwszym uruchomieniem należy wykonać następujące czynności:

1. Utworzyć i aktywować środowisko wirtualne.
2. Zainstalować zależności z pliku `requirements.txt`.
3. Ustawić własny `SECRET_KEY` w pliku `config.py`.
4. Ustawić własny `ADMIN_PASSWORD` w pliku `config.py`.
5. Ustawić prawidłową ścieżkę do bazy danych w polu `DB`.
6. Uruchomić skrypt `init.sql`, aby utworzyć tabele.
7. Dodać dane pracowników do tabeli `pracownicy`.
8. Uruchomić aplikację poleceniem `python app.py`.
9. Otworzyć aplikację przez `http://localhost:5000`.

Bez utworzenia tabel i dodania danych pracowników rejestracja czasu pracy nie będzie działała poprawnie.

---

# Technologie

Projekt wykorzystuje:

* Python,
* Flask,
* SQLite,
* HTML5,
* CSS3,
* JavaScript.

---

# Architektura

Projekt został podzielony zgodnie z zasadami programowania obiektowego:

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

Każda warstwa ma osobną odpowiedzialność:

* **Controller** – obsługa żądań HTTP,
* **Service** – logika biznesowa,
* **Repository** – komunikacja z bazą danych,
* **Model** – reprezentacja danych,
* **Database** – konfiguracja połączenia z bazą SQLite.
