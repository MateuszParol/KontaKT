# Plan 4.1: Optymalizacja Wydajności Widoków (Top 100)

## Objective
Przywrócenie użyteczności programu w obliczu dużych zbiorów danych (szczególnie w zakładach `Plan Kont` i `Historia`). CustomTkinter nie radzi sobie z renderowaniem tysięcy obiektów wewnątrz `ScrollableFrame`. Wymagane jest ograniczenie ładowania bazy i dodanie prostego filtru (Search Bar).

## Requirements
- Okna `AccountsView`, `ContractorsView`, i `HistoryView` muszą otrzymać nowy pasek `CTkEntry` słurzący za wyszukiwarkę.
- Peewee `.select()` musi ładować tylko `~100` pierwszych wyników na podstawie aktywnego filtru.
- Jeśli pole wyszukiwania jest puste - lista ukaże 100 najnowszych/najważniejszych. Tabela ma ładować na nowo kafelki przy każdorazowej zmianie wpisywanej wartości w komponencie Search (debouncing lub event opuszczenia pola).

## Dependencies
- `customtkinter`
- Peewee (operatory `like`)

## Tasks
1. **Modyfikacja `src/kontakt/ui/views/accounts.py` (Konta)**:
   - Dodaj w `header_frame` (lub pod nim) widget: `entry_search = ctk.CTkEntry(..., placeholder_text="Szukaj konta...")`.
   - Zmień `Account.select()` w metodzie `refresh_list()` by uwzględniał filtr `.where(Account.name.contains(phrase) | Account.symbol.contains(phrase))` ograniczając `limit(100)`.
   - Podepnij `entry_search.bind("<KeyRelease>", self.on_search)` by wywołać odświeżenie (dodaj lekkie opóźnienie w przypadku wciskania milisekunda po milisekundzie jeśli to będzie opłacało zablokowanie dławienia, chociaż ograniczenie bazy zlikwiduje lagi).

2. **Modyfikacja `src/kontakt/ui/views/history.py` (Historia)**:
   - Dodaj podobny `entry_search` w sekcji Header.
   - Zmień `Invoice.select()` tak by brał pod uwagę opis lub numer faktury np. `.where(Invoice.number.contains(phrase) | Invoice.description.contains(phrase)).limit(100)`.

3. **Modyfikacja `src/kontakt/ui/views/contractors.py` (Kontrahenci)**:
   - Upewnij się, że widok ten również wspiera okienko `entry_search`.
   - Dodaj .where(`Contractor.name.contains(phrase) | Contractor.nip.contains(phrase)`).limit(100) i użyj odświeżnika.

4. **Weryfikacja**:
   - Odpalenie aplikacji i masowe dodanie zaciągniętej bazy skutkuje renderowaniem interfejsu w mniej niż sekundę (zamiast kilkudziesięciu sekund jak przy 20tys rekordow). Pasek szukania natychmiastowo pozwala zmienić zbiór.
