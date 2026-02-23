# STATE.md

> **Status**: `ACTIVE`
> **Last Update**: Phase 2 Complete

## Context
Projekt w fazie realizacji. Zakończono Fazę 2 (Silnik AI). Zaimplementowano model ML (TF-IDF + MultinomialNB), który przelicza w wątkach prawdopodobieństwa kont (WN/MA) i prezentuje je użytkownikowi w komponencie UI formularza dodawania nowej faktury. Dodano zapisywanie niezbędnych rekodów powiązanych `InvoiceLine`, co umożliwia programowi zdobywanie historii do nauki offline.

## Current Position
- **Phase**: 2 (Completed)
- **Task**: Execution complete
- **Status**: Ready for Phase 3 (Eksport i Raportowanie)

## Next Steps
1. /plan 3 - Plan Phase 3 (Eksport i Raportowanie).

## Last Session Summary
Wykonano Fazę 2 (AI Engine).
- Zainstalowano `scikit-learn`.
- Utworzono moduł `AIEngine` z klasyfikatorem uaktualniającym się on-the-fly.
- Wdrożono w pełni wspieraną formatkę CustomTkinter dodawania nowej faktury z obsługą sugerowania kont.
