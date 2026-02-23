# DECISIONS.md

## ADR-001: Wybór Technologii
**Status**: Proposed
**Kontekst**: Aplikacja desktopowa, offline, "inteligentna", dla Windows.
**Decyzja**: Python + CustomTkinter (lub Flet).
**Uzasadnienie**:
- Python posiada najlepsze biblioteki do ML/AI (`scikit-learn`, `numpy`).
- CustomTkinter zapewnia nowoczesny wygląd (Dark Mode, zaokrąglenia) przy zachowaniu prostoty Tkinter.
- Łatwość tworzenia jednego pliku .exe (PyInstaller).
- Brak konieczności uruchamiania osobnego serwera backendu (jak w Electron).
