# Plan 3.2: Widok Historii Operacji i Eksport (PDF, Excel)

## Objective
Przygotowanie funkcjonalności przeglądania zapisanych "Poleceń Księgowania", czyli Faktur + ich rozksięgowań z AI/Manuala z bazy z opcją zrobienia czytelnego PDF (wydruku) oraz zestawienia dla głównej księgowej w postaci `.xlsx`.

## Requirements
- Widok `HistoryView` na Sidebarze, zawierający zwięzłą tabelę `Invoice`.
- Możliwość naciśnięcia "Drukuj PK (PDF)", który łączy dane i rzuca plikiem w wybrane przez użytkownika miejsce.
- Możliwość "Eksportuj wszystko (Excel)" wyciągające dziennik dekretacji na zewnątrz.

## Dependencies
- `fpdf2` dla PDF Polecenia Księgowania.
- `openpyxl` by `pandas.to_excel()` działał tworząc XMLowe nowoczesne Excele `.xlsx`.

## Tasks
1. **Zaktualizuj `requirements.txt`**:
   - Dodanie pakietu `fpdf2` oraz `openpyxl`.

2. **Nowy Widok Historii (`src/kontakt/ui/views/history.py`)**:
   - Czysty widok tabelaryczny podobny do AccountsView.
   - Lista wyciągnięta z zapytania `Invoice.select().order_by(Invoice.date_issue.desc())`.
   - Do każdego rekordu doczepiony guzik akcji "Pobierz PDF".

3. **Dodanie nowej pozycji w Sidebarze (`src/kontakt/ui/views/sidebar.py`) i `app.py`**:
   - Dodaj pozycję "Historia operacji", mapującą na widok History.

4. **Generator PDF (Polecenie Księgowania) ułożony jako np. `src/kontakt/services/exporter.py`**:
   - Używa `fpdf2` (`from fpdf import FPDF`).
   - Tworzy klasyczną tabelkę informacyjną z Nagłówkiem: np. "Polecenie księgowania dla dokumentu XYZ".
   - Wypisuje: "Nr dok: [Invoice.number]", "Data: [Invoice.date_issue]", "Kwota: [Invoice.amount]".
   - Wypisuje dolną tabelę rozbicia przez powiązane obiekty w Peewee: `lines = invoice.lines`. Wyciąga z nich WN (z symbolu relacji) i MA (symbol relacji).

5. **Eksport Dziennika Księgowań do Excela (`src/kontakt/services/exporter.py`)**:
   - Buduje `pd.DataFrame` scalając wszystkie Faktury po kolei i wyrzucając ładny arkusz poprzez polecenie `df.to_excel(filepath, engine='openpyxl', index=False)`.
   - Odpowiedni przycisk globalny na Historii wywołujący okienko zapisu.

6. **Weryfikacja**:
   - Ręczne wygenerowanie PDF z przykładowej dodanej już wcześniej do bazy Faktury i udowodnienie otwarcia pliku PDF/Excel poleceniem systemowym po poinformowaniu użytkownika o wykonaniu akcji (otwarcie wizualne).
