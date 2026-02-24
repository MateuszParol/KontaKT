# Research: Integracje Excel (.xls/.xlsx) i PDF dla KontaKT (Faza 3)

Zgodnie z wymogami projektu określonymi w `DECISIONS.md` oraz `ROADMAP.md`, Faza 3 zakłada obsługę starych (i nowych) plików MS Excel oraz generowanie dokumentów PDF (Polecenia Księgowania).

## 1. Importowanie starych plików `.xls` (Dane kont)

Plik dostarczony przez jednostkę to tradycyjny binarny `.xls` (format sprzed Excel 2007). 
Standardowe biblioteki typu `openpyxl` obsługują tylko nowe pliki XML-based (`.xlsx`). Aby odczytać plik `.xls`, Python musi skorzystać z innej biblioteki.

**Rozwiązanie:**
Najlepszym standardowym i relatywnie bezpiecznym połączeniem w ekosystemie danych jest użycie **`pandas`** połączonego z silnikiem **`xlrd`**. `xlrd` w wersji >= 2.0 ograniczyło wsparcie wyłącznie do starych plików `.xls` (ze względów bezpieczeństwa), co idealnie wpasowuje się w nasz format.

- Wymagane paczki w `requirements.txt`: `pandas`, `xlrd`
- Kod parsowania sprowadzi się do m.in: `df = pandas.read_excel('plik.xls', engine='xlrd')`.

**Konwersja na modele Peewee (Model `Account`):**
Zgodnie z ustaleniami na dokumencie importowane mają być kolumny: 
1. `WY_KONTO` (ignorowane)
2. `KONTO` (zapisywane jako `Account.symbol`)
3. `WY_NAZWA` (zapisywane jako `Account.name`)

Import powinien wspierać ignorowanie (lub nadpisywanie) duplikatów poprzez blok `try/except` (Peewee `IntegrityError`) lub `insert_many` z klauzulą ON CONFLICT IGNORE (zależnie od tego co wspiera SQLite w Peewee). W prostym ujęciu iteracja z `Account.get_or_create(...)` będzie najbezpieczniejsza.

## 2. Eksportowanie do PDF

Dla generowania prostych, ustrukturyzowanych dokumentów z tabelkami i tekstami stałymi (Polecenie Księgowania to dowód księgowy), biblioteka `reportlab` lub nowsza, prostsza `fpdf2` sprawdza się najlepiej w Pythonie i nie ma żadnych zewnętrznych zależności binarnych (jak np. WeasyPrint wymagający GTK). 

**Rozwiązanie:**
Wykorzystamy `fpdf2` za jego nowoczesne, pythonowe podejście, znakomite wsparcie dla Unicode'u i proste tworzenie tabel w porównaniu do surowego ReportLaba. Będzie wymagać instalacji `fpdf2`.

## 3. Eksportowanie do Excela (Zestawienia)

Wykorzystamy dodaną wcześniej bilbiotekę `pandas` ze standardowym silnikiem eksportowym `openpyxl` (zapis do zdatnego, nowoczesnego formatu `.xlsx` będzie lepszym standardem dla raportów wyjściowych z systemu).

- Wymagane paczki uzupełniające: `openpyxl`

## Podsumowanie Paczek do Fazy 3:
- `pandas`
- `xlrd` (dla odczytu .xls w pandas)
- `openpyxl` (dla zapisu .xlsx w pandas)
- `fpdf2` (dla zapisu Poleceń Księgowania w .pdf)
