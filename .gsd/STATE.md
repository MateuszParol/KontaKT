# STATE.md

> **Status**: `ACTIVE`
> **Last Update**: Phase 2 Complete

## Context
Projekt w fazie realizacji. Zakończono Fazę 2 (Silnik AI). Zaimplementowano model ML (TF-IDF + MultinomialNB), który przelicza w wątkach prawdopodobieństwa kont (WN/MA) i prezentuje je użytkownikowi w komponencie UI formularza dodawania nowej faktury. Dodano zapisywanie niezbędnych rekodów powiązanych `InvoiceLine`, co umożliwia programowi zdobywanie historii do nauki offline.

## Current Position
- **Phase**: 4 (Completed)
- **Task**: Execution complete
- **Status**: Ready for Phase 5 (Polish & Deploy, tworzenie exeka)

## Next Steps
1. /plan 5 - Plan Phase 5 (Polish & Deploy).

## Last Session Summary
Wykonano Fazę 3 (Eksport i Import).
- Wdrożono biblioteki `pandas`, `xlrd`, `fpdf2`, `openpyxl`.
- Utworzono funkcjonalność importowania początkowej bazy kont (`Account`) z pliku starego Excela `.xls` do bazy z poziomu przycisku "Importuj z Excela".
- Dodano widok "Historia Operacji", wyświetlający tabelę połączonych faktur.
- Wygenerowano procesy służące do rzucania Poleceniami Księgowymi (na starym czarno-białym wzorcu księgowym jako wyjście dla urzędów) do plików `.pdf` poszcególnej faktury, oraz zestawień zbiorczych Dziennika operacji do Excela `.xlsx`.
