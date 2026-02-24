# ROADMAP.md

> **Current Milestone**: v2.0 (Rozbudowa i KSeF)
> **Goal**: Wprowadzenie obsługi wielu typów dokumentów księgowych, poprawa ergonomii wprowadzania danych (UX) oraz stworzenie modułu do wystawiania własnych faktur z funkcją eksportu KSeF (XML).

## Must-Haves
- [x] Nawigacja górna (Navbar) obok/zamiast Sidebar'a dla zwiększonej liczby funkcji.
- [x] Obsługa wielu typów dokumentów (wyciągi, noty, wyciągi bankowe) - rozszerzenie księgowania poza same faktury zakupowe.
- [ ] Szybkie wybieranie ostatnich kont (np. podwójne kliknięcie) i klonowanie pozycji dekretacji, dla seryjnego wprowadzania podobnych pozycji.
- [ ] Naprawa importu kontrahentów (usunięcie ".0" z formatu NIP).
- [ ] Wystawianie faktur ustrukturyzowanych (Kreator faktur sprzedaży z exportem do XML dla KSeF).

## Phases

### Phase 1: Nawigacja i Różne Typy Dokumentów
**Status**: ⬜ Not Started
**Objective**: Wdrożenie paska nawigacyjnego (Navbar) u góry ekranu i reorganizacja widoków. Rozbudowa modelu bazy danych o typy dokumentów (zastąpienie sztywnego `Invoice` uniwersalnym `Document`).

### Phase 2: Poprawki UX - Ergonomia wprowadzania danych
**Status**: ⬜ Not Started
**Objective**: Wdrożenie pamięci ostatnio użytych kont i możliwości kliknięcia aby szybko je wybrać. Wprowadzenie funkcji "Dodaj kolejną pozycję" / powielania wierszy dekretacji. Poprawka konwersji typów w imporcie z Excela (naprawa NIP).

### Phase 3: Moduł Sprzedaży (Kreator Faktur)
**Status**: ⬜ Not Started
**Objective**: Utworzenie okna wystawiania własnych faktur. Dodawanie rzędów asortymentu, liczenie podatku VAT.

### Phase 4: Integracja KSeF (Eksport XML)
**Status**: ⬜ Not Started
**Objective**: Implementacja mappera i eksportera danych wystawionej faktury na schemat ustrukturyzowany KSeF (XML).
