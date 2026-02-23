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

### Phase 4: Polish & Deploy
**Status**: ⬜ Not Started
**Cel**: Przygotowanie wersji instalacyjnej dla użytkownika końcowego.
**Wymagania**:
- [ ] Instalator Windows (.exe).
- [ ] Dokumentacja użytkownika (Instrukcja).
- [ ] Testy na "czystym" systemie Windows.
