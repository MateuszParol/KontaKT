# Plan 4.2: Import Kontrahentów z Excela

## Objective
Dostarczenie interfejsu (analogicznego do Planu Kont w Fazie 3) do ładowania pliku bazy kontrahentów w Excelu do wewnętrznej bazy SQLite (Tabela `Contractor`). Import musi poradzić sobie ze zbitką wielu komórek adresowych w jedną na potrzeby zachowania obecnego 3-kolumnowego układu modelu.

## Requirements
- Moduł `importer.py` posiada nową funkcję obsługującą plik Excel Kontrahentów.
- Kolumny to: *Kod, Nazwa skrócona, Pełna nazwa, Miejscowość, Ulica, Kod pocztowy, NIP, REGON/PESEL, Zablokowany.*
- Widok `ContractorsView` dostaje przycisk pozwalający wczytać plik z odpaleniem logiki.

## Database Constraints mapping
- `Pełna nazwa` -> wpisana do pola bazodanowego `name`. (Jeżeli nie istnieje, to zapożyczyć z `Nazwa skrócona`).
- `Ulica, Kod pocztowy Miejscowość` -> sklejane i rzucane ostatecznie w jedno pole bazy `address`.
- `NIP` -> pole bazodanowe `nip`

## Tasks
1. **Rozbudowa funkcjonalności `src/kontakt/services/importer.py`**:
   - Tworzenie: `import_contractors_from_excel(filepath: str) -> tuple[int, str]`.
   - Oczekiwane wymagane kolumny `NIP`, `Pełna nazwa` (z awaryjnym wykorzystaniem 'Nazwa...', 'Ulica' etc.).
   - Przeiteruj się po `df.iterrows()`. Połącz do zmiennej `address` odpowiednie składowe pliku np. `Ulica`, `Kod pocztowy`, `Miejscowość` (sprawdzając czy nie są `NaN`).
   - Wywołaj zabezpieczony update `Contractor.get_or_create(...)`.

2. **Podłączenie UI w `src/kontakt/ui/views/contractors.py`**:
   - Wygeneruj, analogicznie do Planu 3.1, zgrabny guzik w Header Frame: "Importuj z Excela".
   - Przekieruj pod niego okenko `filedialog.askopenfilename()`.
   - Dodaj Label wyświetlający status i w razie sukcesu przeładuj zopytymalizowaną (Zad 4.1) listę.

3. **Weryfikacja**:
   - Przycisk pojawia się w strefie "Kontrahenci". Silnik przepuszcza pliki .xls z nagłówkami. Równoważy brakujące pola adresowe nie rzucając NullPointerów do SQL.
