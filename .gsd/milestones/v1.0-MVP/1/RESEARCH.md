# RESEARCH.md

> **Phase**: 1
> **Topic**: Project Structure & Technology Stack (Python + CustomTkinter)

## Cel
Ustalenie optymalnej struktury projektu dla aplikacji desktopowej z planowanym modułem AI i lokalną bazą danych, aby uniknąć problemów z refaktoryzacją w przyszłości.

## Ustalenia Techniczne

### 1. Struktura Katalogów
Zastosujemy strukturę "src-layout" dla lepszej separacji pakietów i łatwiejszego pakowania PyInstallerem.

```
KontaKT/
├── src/
│   ├── kontakt/
│   │   ├── __init__.py
│   │   ├── main.py           # Entry point
│   │   ├── config.py         # Konfiguracja (ścieżki, stałe)
│   │   ├── database/         # Warstwa danych
│   │   │   ├── __init__.py
│   │   │   ├── db.py         # Połączenie SQLite
│   │   │   └── models.py     # Modele (Peewee lub surowe SQL) -> Wybór: Peewee ORM (prostsze niż SQLAlchemy, wystarczające)
│   │   ├── ui/               # Interfejs (CustomTkinter)
│   │   │   ├── __init__.py
│   │   │   ├── app.py        # Główna klasa App(ctk.CTk)
│   │   │   ├── styles.py     # Kolory, fonty
│   │   │   └── views/        # Widoki (Ekrany)
│   │   │       ├── dashboard.py
│   │   │       ├── invoice_add.py
│   │   │       └── accounts.py
│   │   └── services/         # Logika biznesowa & AI
│   │       ├── ai_service.py # Proxy do modelu
│   │       └── data_importer.py
├── assets/                   # Ikony, obrazy
├── data/                     # Lokalne pliki (Baza danych .db użytkownika)
├── tests/                    # Testy pytest
├── requirements.txt
├── README.md
└── .gitignore
```

### 2. Biblioteki (Core Stack)
-   **GUI**: `customtkinter` (nowoczesny wygląd), `packaging`, `Pillow` (obsługa obrazów).
-   **Database**: `peewee` (lekki ORM, idealny do SQLite i desktopów).
-   **AI (Phase 2 prepare)**: `scikit-learn`, `pandas`, `numpy` (dodane później, ale struktura musi być gotowa).
-   **Utility**: `platformdirs` (do poprawnego zapisu danych w AppData na Windows).

### 3. Wzorce Projektowe
-   **MVC / MVVM**: UI (`views`) oddzielone od logiki bazy danych (`database`). `App` zarządza stanem globalnym i nawigacją.
-   **Dependency Injection (Light)**: Przekazywanie instancji bazy/serwisów do widoków, zamiast globalnych importów (ułatwi testowanie).

## Decyzje do Planowania
1.  **ORM**: Użyjemy `peewee` zamiast czystego SQL dla bezpieczeństwa i szybkości developmentu.
2.  **Config**: Użycie `platformdirs` jest krytyczne, aby aplikacja działała poprawnie po zainstalowaniu (baza danych nie może być w `Program Files`).

## Plan Implementacji (Faza 1)
1.  **Fundamenty**: Setup venv, git, struktura katalogów (src), config.
2.  **Baza Danych**: Modele Peewee (Faktura, Kontrahent, Konto), migracje (automatyczne tworzenie tabel).
3.  **UI Core**: Główne okno, nawigacja (Sidebar), placeholder views.
4.  **UI Funkcjonalne**: Formularze dodawania danych i zarządzania planem kont.
