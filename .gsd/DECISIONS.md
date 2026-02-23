## Phase 3 Decisions

**Date:** 2026-02-23

### Scope
- **Import danych początkowych (Plan Kont z Excela):** Uznano za konieczność (bloker użyteczności). Użytkownik chce importować pliki `.xls` z układem: `WY_KONTO` (nr numeryczny, nieistotny), `WY_NAZWA` (nazwa konta), `KONTO` (prawidłowy symbol konta).

### Approach
- Chose: Opcja B - Przycisk w GUI "Importuj z Excela" w widoku Konta (`AccountsView`), dla ułatwienia pracy osobom nietechnicznym. Odczyt przez `pandas`/`xlrd`.

### Constraints
- Plik w formacie `.xls` (zazwyczaj wymaga `xlrd` w pandach, w nowszych wersjach pandas zalecany jest openpyxl ale nie dla starego .xls). Należy upewnić się o odpowiednich zależnościach. Import ma stanowić część Fazy 3.
