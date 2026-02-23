# Plan 5.2: Usprawnienie okien wyboru z pop-up search (InvoicesView)

## Objective
Kiedy użytkownik dodaje fakturę i otwiera Dropdown `CTkOptionMenu` do wyboru Kontrahenta lub konta, z racji braku limitów okno zajmie całą wysokość ekranu bez mozliwości sensownego filtrowania (Szukania) - jest to wina samej koncepcji CustomTkintera. Lepszym i bardziej zoptymalizowanym rozwiązaniem jest zastąpienie przycisku na modalne okno "Wybierz...".

## Requirements
- Formularz dodawania faktury w `InvoicesView` posiadał wybór pól za pomocą `CTkOptionMenu`. Należy zmienić ten widget na sztywny tekst/parametr pokazujący "Wybrano:...", oraz guzik `Zmień`.
- Guzik `Zmień` odpala Toplevel window (Custom Toplevel).
- Okno popup to wycinek implementacji Listowego `Treeview` z Planu 5.1 (Wyszukiwarka + Lista obiektów) oraz ukrytym polem zapisu wartości do rodzica po podwójnym kliknięciu wiersza w Toplevel widoku.

## Tasks
1. **Model popup_list.py (Komponent Wielokrotnego Użytku)**:
   - Zbuduj nowy widok pomocniczy/moduł: `src/kontakt/ui/components/popup_list.py` zawierający uniwersalne okienko Searcher:
     - Parametry: `title`, `data(lista slownikow)`, `on_select(callback)`.
     - Toplevel ma pole CTkEntry na górze i duży Listbox (lub Treeview) na podgląd wyników.
     - Filtr na `on_change`.
     - `Double-click` pobiera ID elementu, odpala `on_select` i niszczy `Toplevel()`.

2. **Podpięcie InvoicesView**:
   - `self.opt_contractor`, `self.val_wn`, `self.val_ma` - zamiast nich dajemy `CTkLabel` (lub `CTkEntry` readonly) i mały przycisk "Wybierz".
   - Naciśnięcie wywołuje klasę Popupu z przekazaniem bazy kontraktów (lub odpowiednich kont dla dekretacji). Funkcja callback uaktualni nowo wybraną pozycję na formie (np. w specjalnej zmiennej przypisanej do klasy GUI `self.selected_contractor_id` itd).

3. **Poprawka w zapisywaniu w `add_invoice()`**:
   - Podczas dodawania nowej faktury wyciągajemy `self.selected_contractor.id` (kontrahenta) oraz `self.selected_wn_account.id` zamieniając dotychczasowe `get()` z `OptionMenu`.

## Verification Plan
Odpalić GUI i próbować wejść w formularz. Wybranie Konta "Zmień" winno wyświetlić okienko z podanymi dostępnymi obiektami, a dwuklik ustawi jego nazwę na panelu faktur. Dodawanie fakury zakończone sukcesem po wybraniu wszystkiego jak do tej pory.
