# Plan 5.1: Zastąpienie CTkScrollableFrame natywnym ttk.Treeview

## Objective
Znaczna poprawa wydajności programu przy wyświetlaniu obszernych widoków listowych (Konta, Kontrahenci, Historia). CustomTkinter dla każdego wpisu w bazie tworzy dziesiątki instancji widżetów GUI i umieszcza je w ramce z suwakiem, co prowadzi do drastycznych zawieszeń. `ttk.Treeview` rozwiązuje ten problem.

## Requirements
- Przebudowa sekcji "List Area" w plikach:
  - `src/kontakt/ui/views/accounts.py`
  - `src/kontakt/ui/views/contractors.py`
  - `src/kontakt/ui/views/history.py`
- Zastosowanie natywnego widżetu z Tcl/Tk - `ttk.Treeview` z dołączonym klasycznym suwakiem `ttk.Scrollbar` (lub `ctk.CTkScrollbar`).
- Przywrócenie ładowania całej bazy danych dla tych okien (usunięcie `.limit(100)`).
- Dostosowanie kolorystyki `Treeview` używając `ttk.Style()` tak, aby element ten pasował do ciemnego motywu CustomTkintera.

## Tasks
1. **Konfiguracja Stylu (Theme)**:
   - W punkcie wejścia (lub metodach `__init__` poszczególnych widoków) użyj `style = ttk.Style()`.
   - Zmień tło tabeli i elementów `style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0)` oraz wierszy naprzemiennych/nagłówków.

2. **Refaktoryzacja AccountsView**:
   - Zastąpić `self.scroll_frame = ctk.CTkScrollableFrame(...)` ramką główną, w której osiądą: `self.tree = ttk.Treeview(..., columns=("Symbol", "Nazwa"), show="headings")` i `scrollbar`.
   - W procedurze `refresh_list` używać `self.tree.insert("", "end", values=(acc.symbol, acc.name))`.
   - Usunąć stary zapis limitu 100 z wiersza pobierania obiektów. Wyszukiwarka (`entry_search`) wciąż ma działać filtrując listę.

3. **Refaktoryzacja ContractorsView**:
   - Analogicznie jak wyżej, kolumny: ("Nazwa", "NIP").
   - Brak limitów. Filtrowanie działające na .where() odświeża poprawnie Treeview (po jego wyczyszczeniu np. `self.tree.delete(*self.tree.get_children())`).

4. **Refaktoryzacja HistoryView**:
   - Tu tabela idealnie się wpasuje. Usunąć stare nagłówki w Labelach (`self.cols_frame`). Zastąpić je natywnymi nagłówkami Treeview: `self.tree.heading("Data", text="Data")` itd.
   - Kolumny: ("Data", "Dokument", "Kontrahent", "Kwota").
   - Ponieważ Treeview nie ma łatwo przypisanych przycisków na kafelku do Generowania PDF (jak w historii Fazy 4), musimy wyłapać podwójne kliknięcie uzytkownika `<Double-1>` na wierszu w module zdarzeń. Wtedy program może wygenerować i pokazać PDF-a PK. O tym należy poinformować w instrukcji Labela, np. `(Kliknij dwa razy w rekord, aby wyeksportować fakturę PDF)`.

## Verification Plan
1. Uruchomienie `KontaKT` po modyfikacjach i wejście w "Plan Kont". Moduł powinien wczytać się natychmiastowo z ciemną listą w stylu Excela dla wszystkich elementów bazy, a pasek przewijania pozwoli na nawigację bez spadku klatek/zacięć.
2. Zdarzenia on_search muszą natychmiastowo limitować wyświetlane wiersze w nowym komponencie.
