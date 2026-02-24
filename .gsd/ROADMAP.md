# ROADMAP.md

> **Current Milestone**: v3.0 (Design & UI Overhaul)
> **Goal**: Całkowita przebudowa interfejsu w kierunku nowoczesnego, animowanego i eleganckiego designu bazującego na sprawdzonych schematach kolorystycznych ("Tokyo Night") zachowując wysoką czytelność dla pracy księgowej.

## Must-Haves
- [ ] Zintegrowany system motywów (Light/Dark Mode) z naciskiem na "Tokyo Night" (głębokie granaty, fiolety, neony).
- [ ] Płynna animacja przełączania motywu (np. rozlany kolor z rogu ekranu, fade-in/out).
- [ ] Subtelne, animowane "pływające" tło w głównych rejonach nawigacyjnych, niewchodzące w obszar roboczy (np. za Navbarem lub na ekranie startowym).
- [ ] Nowoczesny design komponentów (drzewa, inputy, przyciski) z hover-efektami.
- [ ] Czytelność kontrastów – design nie może męczyć wzroku podczas wprowadzania kilkudziesięciu faktur z rzędu.

## Phases

### Phase 1: Architektura Motywów i Główne Kolory
**Status**: ⬜ Not Started
**Objective**: Wdrożenie centralnego menedżera Themingu dla CustomTkinter. Zaprojektowanie palety Tokyo Night (Dark) oraz kompatybilnego motywu Light. Przełączenie głównych kontenerów na nowe kolory.

### Phase 2: Animowane Przejścia i Toggle
**Status**: ⬜ Not Started
**Objective**: Stworzenie niestandardowego przełącznika Light/Dark. Zaimplementowanie animacji "wylewającego się z rogu" gradientu/koloru dla płynnego i satysfakcjonującego przejścia między motywami (wymaga zabawy z warstwami `Canvas` tkinera).

### Phase 3: Pływające Tło i Efekty Wizualne
**Status**: ⬜ Not Started
**Objective**: Dodanie interaktywnego tła z animowanymi elementami (cząsteczki, fale lub bloby) w strefach "pustych" (ekran powitalny, puste przestrzenie nawigacji), omijając okna wprowadzania danych by zachować fokus. Upiększenie przycisków i tabel (Treeview).
