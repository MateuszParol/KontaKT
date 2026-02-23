# Plan 3.1: Import Planu Kont z pliku Excel (.xls)

## Objective
Dodanie użytkownikowi na ekranie `AccountsView` intuicyjnego przycisku pozwalającego wczytać plik binarny `.xls` i automatycznie zasilić tabelę `Account` odpowiednimi numerami Kont, by można było dalej z nich korzystać w formularzu głównym.

## Requirements
- Użytkownik widzi przycisk w widoku Kont.
- Aplikacja otwiera graficzne okienko wyboru pliku (ograniczone do Excel - .xls/.xlsx).
- Aplikacja czyta kolumny `WY_KONTO` (ignoruje u nas, ale sprawdza strukturę), `KONTO` (nr) oraz `WY_NAZWA` z pliku i dopisuje je do bazy danych wykorzystując bezpieczne ładowanie/aktualizacje w ORM Peewee.

## Dependencies
- `pandas` (Czytanie ramek danych)
- `xlrd` (Silnik dla binarnego, starszego .xls, co najmniej w wersji 2.0.1)
- Pythonowe GUI: `customtkinter.filedialog`

## Tasks
1. **Zaktualizuj `requirements.txt`**:
   - Dodaj dopisy nowych bibliotek niezbędnych do działania (`pandas`, `xlrd`).

2. **Przygotuj serwis importu (`src/kontakt/services/importer.py` lub pododna funkcja pomocnicza)**:
   - Funkcja `import_accounts_from_excel(filepath: str) -> (int, str)` która:
      - Wczyta DataFrame `pd.read_excel(filepath, engine='xlrd')`.
      - Odfiltruje tylko te wiersze, które posiadają zmapowane odpowiednio kolumny `KONTO` i `WY_NAZWA`.
      - Zrobi iteracyjne `Account.get_or_create(symbol=..., defaults={'name': ...})` by nie rzucić wyjątkiem na istniejące wpisy.
      - Zwróci ilość dodanych kont, lub rzuci wyjątek z błędem w razie złego pliku.

3. **Zmodyfikuj `AccountsView` (`src/kontakt/ui/views/accounts.py`)**:
   - Dodaj nowy przycisk na dole/na górze tabeli: "Importuj z Excela (xls)".
   - Podepnij callback pod okienko `ctk.filedialog.askopenfilename(filetypes=[("Pliki Excel", "*.xls *.xlsx")])`.
   - Podłącz logikę z serwisu, pokaż komunikat o sukcesie i wywołaj lokalne odświeżenie `refresh_accounts()`.

4. **Weryfikacja**:
   - Skrypt odpala się bez błędów. Użytkownik ma panel informacyjny gotowy. Kod pozwala załadować prosty sztuczny arkusz .xls (możliwe utworzenie takowego podczas wykonywania testów) i wyświetla poprawnie odświeżoną listę w widoku aplikacji.
