## Phase 3 Decisions

**Date:** 2026-02-23

### Scope
- **Import danych początkowych (Plan Kont z Excela):** Uznano za konieczność (bloker użyteczności). Użytkownik chce importować pliki `.xls` z układem: `WY_KONTO` (nr numeryczny, nieistotny), `WY_NAZWA` (nazwa konta), `KONTO` (prawidłowy symbol konta).

### Approach
- Chose: Opcja B - Przycisk w GUI "Importuj z Excela" w widoku Konta (`AccountsView`), dla ułatwienia pracy osobom nietechnicznym. Odczyt przez `pandas`/`xlrd`.

### Constraints
- Plik w formacie `.xls` (zazwyczaj wymaga `xlrd` w pandach, w nowszych wersjach pandas zalecany jest openpyxl ale nie dla starego .xls). Należy upewnić się o odpowiednich zależnościach. Import ma stanowić część Fazy 3.

## Phase 4 Decisions

**Date:** 2026-02-23

### Scope
- **Wydajność interfejsu (Lag):** Po wgraniu kompletnego planu kont (lub w historii urosłej z czasem), aplikacja mocno spowalnia. Moduł `CTkScrollableFrame` z biblioteki `customtkinter` nie jest przeznaczony do renderowania tysięcy wierszy na raz. Konieczne jest wprowadzenie wyszukiwarki (Search) oraz limitów zwracanych rekordów (np. ładowanie tylko 100 pierwszych dopasowań).
- **Import Kontrahentów:** Podobnie jak plan kont, użytkownik potrzebuje zaciągnąć bazę kontrahentów z pliku o rozbudowanej strukturze ("Nazwa", "NIP", "Adres" itp). Należy zmapować to do tabeli `Contractor`.

### Approach
- Chose: Dodanie paska wyszukiwania typu (wpisz by wyszukać) do widoków: `AccountsView`, `ContractorsView` i `HistoryView`. Limitowanie zapytań SQL Peewee do max 100 wyników. Dodanie kolejnego guzika "Importuj Kontrahentów" podłączonego pod zaktualizowany `importer.py` zdolny mapować odpowiednie kolumny z Excela na model.

### Constraints
- Model `Contractor` posiada obecnie tylko `nip`, `name`, `address`. Dane z Excela (`Ulica`, `Kod pocztowy`, `Miejscowość`) zostaną połączone w jedno pole `address` (np. "Ulica, Kod Miejscowość"). `Pełna nazwa` trafi do `name`. By nie psuć bazy, nie będziemy zmieniać schematu, a jedynie inteligentnie mapować dane.

## Phase 5 Decisions

**Date:** 2026-02-24 (In Progress)

### Approach
- **Listy (Konta, Kontrahenci, Historia) - Chose:** Zastąpienie CTkScrollableFrame natywnym widgetem **`ttk.Treeview`** przestylowanym pod projekt. Jest to rekomendowane i jedyne rozsądne rozwiązanie umożliwiające ładowanie dziesiątek tysięcy wierszy naraz bez zamrażania UI w CustomTkinter. Limit = brak. Opcja szukajki z Fazy 4 pozostanie jako dynamiczne zawężanie.
**User Confirmation (2026-02-24):** Używamy standardowego `ttk.Treeview` (opcja A) dla maksymalnej wydajności, trzymając kod otwarty na lepszy styling w przyszłym kamieniu milowym.
- **Drop-downy z autouzupełnianiem (Wybrór rekordu) - Chose:** Odrzucenie CTkOptionMenu na rzecz "Modalnego Okienka" (Pop-up Toplevel) wyposażonego w widget wyszukiwania + podgląd Listbox/Treeview. Jest to optymalny UX, umożliwiający w fakturach wpisanie części nazwy by zatwierdzić dany wybór z dużej biblioteki bez pomyłek.
**User Confirmation (2026-02-24):** Zgoda na w pełni modalne (blokujące główne okno) zachowanie pod-okienek wyboru.

### Constraints
- Widget `ttk.Treeview` wymaga własnego podpięcia paska przewijania (Scrollbar) oraz zmiany konfiguracji `style.configure` na ciemne tło by nie psuć DarkMode CustomTkintera. Pamiętać o architekturze gotowej na zmiany (Next Milestone).
