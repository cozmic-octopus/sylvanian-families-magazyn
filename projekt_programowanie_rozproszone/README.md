# Sylvanian Families – System Zarządzania Magazynem

## Opis projektu

Projekt przedstawia system zarządzania magazynem produktów Sylvanian Families, zrealizowany w architekturze mikroserwisowej.

System składa się z dwóch niezależnych mikroserwisów REST API:

1. **Product Service (Serwis Produktów)** – przechowuje informacje o produktach, takie jak nazwa, cena i kategoria.
2. **Stock Service (Serwis Magazynowy)** – przechowuje informacje o liczbie dostępnych produktów i komunikuje się z Serwisem Produktów za pomocą zapytań HTTP.

Dane produktów mają charakter demonstracyjny.

## Technologie

- Python 3.13
- FastAPI
- Uvicorn
- HTTPX
- REST API
- JSON

## Struktura projektu

```text
projekt_programowanie_rozproszone/
│
├── product_service/
│   ├── main.py
│   └── requirements.txt
│
├── stock_service/
│   ├── main.py
│   └── requirements.txt
│
└── README.md
```

## Uruchomienie projektu

### 1. Pobranie repozytorium

```bash
git clone https://github.com/cozmic-octopus/sylvanian-families-magazyn.git
cd projekt_programowanie_rozproszone
```

### 2. Utworzenie środowiska wirtualnego

```bash
py -3.13 -m venv .venv
```

### 3. Aktywacja środowiska

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Jeśli PowerShell blokuje uruchamianie skryptów, można zastosować:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Następnie ponownie aktywować środowisko.

### 4. Instalacja bibliotek

```bash
pip install -r product_service/requirements.txt
pip install -r stock_service/requirements.txt
```

### 5. Uruchomienie Serwisu Produktów

W pierwszym terminalu:

```powershell
cd product_service
python -m uvicorn main:app --reload --port 8001
```

Serwis będzie dostępny pod adresem:

http://127.0.0.1:8001

Dokumentacja API:

http://127.0.0.1:8001/docs

### 6. Uruchomienie Serwisu Magazynowego

W drugim terminalu, po aktywowaniu tego samego środowiska wirtualnego i przejściu do katalogu głównego projektu:

```powershell
cd stock_service
python -m uvicorn main:app --reload --port 8002
```

Serwis będzie dostępny pod adresem:

http://127.0.0.1:8002

Dokumentacja API:

http://127.0.0.1:8002/docs

**Uwaga:** oba mikroserwisy muszą działać jednocześnie.

## Endpointy API

### Serwis Produktów – port 8001

| Metoda | Endpoint | Opis |
|---|---|---|
| GET | `/` | Informacje o serwisie |
| GET | `/products` | Lista produktów |
| GET | `/products/{product_id}` | Pobranie produktu o wskazanym ID |

### Serwis Magazynowy – port 8002

| Metoda | Endpoint | Opis |
|---|---|---|
| GET | `/` | Informacje o serwisie |
| GET | `/stock/{product_id}` | Pobranie informacji o stanie magazynowym produktu |

## Komunikacja między mikroserwisami

Serwis Magazynowy wysyła zapytanie HTTP do Serwisu Produktów, aby sprawdzić, czy produkt o podanym identyfikatorze istnieje.

Jeżeli produkt istnieje, Serwis Magazynowy zwraca jego nazwę, kategorię, cenę oraz ilość dostępnych sztuk.

Jeżeli produkt nie istnieje, zwracany jest status HTTP 404.

W przypadku problemów z komunikacją z Serwisem Produktów obsługiwane są również błędy połączenia.

## Przykładowe testy

| Zapytanie | Oczekiwany rezultat |
|---|---|
| `/stock/1` | 200 OK – produkt istnieje |
| `/stock/4` | 200 OK – produkt istnieje, ilość 0 |
| `/stock/999` | 404 Not Found – produkt nie istnieje |

## Autorka

Projekt wykonany w ramach przedmiotu **Programowanie rozproszone**.
