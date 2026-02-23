# ROADMAP.md

> **Status**: `IN_PROGRESS`
> **Milestone**: v1.0 (MVP)

## Fazy (Phases)

### Phase 1: Fundamenty i Prototyp UI
**Status**: ✅ Complete
**Cel**: Stworzenie działającej aplikacji desktopowej z podstawowym interfejsem i bazą danych.
**Wymagania**:
- [x] Szielet aplikacji (Python + CustomTkinter/Flet).
- [x] Baza danych SQLite (Tabela: Kontrahenci, Operacje, Plan Kont).
- [x] Ekran dodawania nowej faktury (pola: Data, Opis, Kwota, Kontrahent).
- [x] Zarządzanie Planem Kont (CRUD) - *Added in validation*.


### Phase 2: Silnik Inteligencji (AI)
**Status**: ⬜ Not Started
**Cel**: Implementacja mechanizmu uczenia się i sugerowania dekretacji.
**Wymagania**:
- [ ] Implementacja prostego modelu ML (np. Naive Bayes / TF-IDF + Cosine Similarity) na bazie `scikit-learn`.
- [ ] Mechanizm "uczenia się" w locie (po zatwierdzeniu dekretacji przez użytkownika, model się aktualizuje).
- [ ] Wyświetlanie sugestii (Top 3) z procentem pewności.

### Phase 3: Eksport i Raportowanie
**Status**: ⬜ Not Started
**Cel**: Umożliwienie użytkownikowi wykorzystania wyników pracy programu.
**Wymagania**:
- [ ] Import Planu Kont z pliku `.xls` (kolumny `WY_KONTO`, `WY_NAZWA`, `KONTO`) z poziomu GUI.
- [ ] Eksport do PDF (Polecenie Księgowania).
- [ ] Eksport do Excela (Zestawienie dekretacji).
- [ ] Historia operacji z możliwością wyszukiwania.

### Phase 4: Optymalizacja Wydajności i Kontrahenci
**Status**: ⬜ Not Started
**Cel**: Przywrócenie płynności aplikacji na dużych zbiorach danych i wgranie bazy kontrahentów.
**Wymagania**:
- [ ] Ograniczenie list (Konta, Kontrahenci, Historia) do Top 100 wyników.
- [ ] Wdrożenie pól szybkiego wyszukiwania (filtrowania) nad listami.
- [ ] Moduł importu Kontrahentów z Excela (mapowanie kolumn takich jak REGON, NIP, Adres do aktualnego modelu Peewee).

### Phase 5: Reorganizacja GUI - Listy Treeview i Interfejs Faktur
**Status**: ⬜ Not Started
**Cel**: Ekstremalna optymalizacja renderowania list całobazowych przy zachowaniu stylistyki oraz usprawnienie doświadczenia z polami wyboru z tysięcy jednostek.
**Wymagania**:
- [ ] Przebudowa `AccountsView`, `ContractorsView`, `HistoryView` na wysoce wydajne obiekty `ttk.Treeview` zamiast zagnieżdżonych Labeli CustomTkintera. Zniesienie górnych limitów limit(100).
- [ ] Płynne przewijanie do obsługi nawet n-tysięcznych eksportów.
- [ ] Zastąpienie limitowanych Dropdownów (CTkOptionMenu) w widoku `InvoicesView` modalnymi oknami Popup wyposażonymi we własne wyszukiwarki do selekcji Kont i Kontrahentów.

### Phase 6: Polish & Deploy
**Status**: ⬜ Not Started
**Cel**: Przygotowanie wersji instalacyjnej dla użytkownika końcowego.
**Wymagania**:
- [ ] Instalator Windows (.exe).
- [ ] Dokumentacja użytkownika (Instrukcja).
- [ ] Testy na "czystym" systemie Windows.
