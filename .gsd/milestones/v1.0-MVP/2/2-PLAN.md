---
phase: 2
plan: 2
wave: 2
depends_on: ["1"]
files_modified: ["src/kontakt/ui/views/invoice_add.py", "src/kontakt/ui/app.py"]
autonomous: true

must_haves:
  truths:
    - "Użytkownik widzi sugestie kont i paragrafów na ekranie dodawania faktury po wpisaniu opisu"
    - "Domyślnie podpowiadane są wartości z największym prawdopodobieństwem"
  artifacts:
    - "Zmodyfikowany widok src/kontakt/ui/views/invoice_add.py zawiera elementy UI dla sugestii"
  key_links:
    - "Zdarzenie wpisywania (lub utraty ostrości) w polu 'Opis' wyzwala akcję z `AIEngine.predict`"
---

# Plan 2.2: Integracja AI z Interfejsem Użytkownika

<objective>
Podpięcie silnika sztucznej inteligencji pod formularz dodawania faktury. Po wprowadzeniu opisu przez użytkownika, formularz powinien odpytać silnik i zasugerować optymalną dekretację (konta WN/MA).

Purpose: Dostarczenie realokowanej wartości dodanej dla użytkownika końcowego - wyręczenie go w ręcznym szukaniu kont poprzez automatyczne sugestie.
Output: Podpięty AIEngine do formularza `invoice_add.py`. Reaktywny interfejs wyświetlający pobrane przypuszczenia.
</objective>

<context>
Load for context:
- .gsd/SPEC.md
- src/kontakt/ui/views/invoice_add.py
- src/kontakt/ai/engine.py (stworzone w planie 1)
</context>

<tasks>

<task type="auto">
  <name>Inicjalizacja i wpięcie AIEngine w widok</name>
  <files>src/kontakt/ui/views/invoice_add.py, src/kontakt/ui/app.py</files>
  <action>
    Zainicjuj `AIEngine` na poziomie aplikacji (w `app.py`) aby model załadował się/odświeżył w tle przy starcie, a następnie przekaż referencję lub udostępnij metodę predykcji dla `InvoiceAddView`.
    W widoku `InvoiceAddView` dodaj nasłuchiwanie na pole tekstowe `Opis` (np. przycisk "Sugeruj dekretację" obok pola lub po stracie ostrości pod warunkiem min. 3 znaków).
    AVOID: Blokowania głównego wątku UI (`CustomTkinter` mainloop). Inicjalizacja lub odpytanie bazy w `engine.py` powinno dziać się w tle (threading) lub być zoptymalizowane tak, aby nie powodować "zacięcia" przycisku.
  </action>
  <verify>python -c "from kontakt.ui.views.invoice_add import InvoiceAddView"</verify>
  <done>Pole opisu ma wpiętą akcję (np. FocusOut), która wywołuje `engine.predict()`.</done>
</task>

<task type="auto">
  <name>Prezentacja Sugestii w UI</name>
  <files>src/kontakt/ui/views/invoice_add.py</files>
  <action>
    Rozbuduj formularz dodawania faktury o dedykowaną, czytelną sekcję "Sugestie AI". 
    Sekcja ta, początkowo ukryta lub oznaczona statusem "Brak opisu", powinna po odebraniu `Top 3` wyników od `AIEngine` zaktualizować się, pokazując karty/przyciski z zestawem [Konto Wn, Konto Ma] oraz % pewności.
    Po kliknięciu w konkretną sugestię, pola wyboru Kont WN i Kont MA w głównej części formularza linii dekretacji muszą się automatycznie uzupełnić/ustawić na te wartości.
    Gdy % pewności jest wysoki (>80%), automatycznie podświetl tę opcję jako domyślną.
  </action>
  <verify>grep -A 5 "Sugestie AI" src/kontakt/ui/views/invoice_add.py</verify>
  <done>Wyniki od MLa są parsowane przez UI i ułatwiają jedno-klikowe wypełnienie formatki.</done>
</task>

</tasks>

<verification>
After all tasks, verify:
- [ ] UI wyświetla sekcję podpowiedzi po przejściu z pola `Opis`.
- [ ] Wybranie kliknięciem danej podpowiedzi aktualizuje Comboboxy/Entry kont.
</verification>

<success_criteria>
- [ ] All tasks verified
- [ ] Must-haves confirmed
</success_criteria>
