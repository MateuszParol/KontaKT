# Research: Silnik ML dla KontaKT (Faza 2)

Zgodnie z protokołem planowania to jest zadanie na poziomie 2 (Standard Research), ponieważ wprowadzamy nową integrację - `scikit-learn` do obsługi analizy danych z bazy SQLite.

## Analiza wymagań z SPEC.md

1. **Cel:** Sugestia kont i paragrafów na podstawie opisu faktury.
2. **Offline-first:** Model trenowany i predykcje odpytywane lokalnie (narzuca brak zewnętrznych API AI typu OpenAI).
3. **Wolumen:** 50-100 dokumentów miesięcznie (bardzo mały zbiór danych), co wymusza proste, szybkie douczanie i lekkie modele zamiast deep learningu.

## Rekomendowany Stos Technologiczny

**Scikit-learn** wraz z **joblib** (do zapisu stanu modelu).
- **Procesowanie tekstu:** `TfidfVectorizer` (zamiana opisu tekstowego na cechy numeryczne).
- **Klasyfikator:** Wymagamy modelu, który potrafi zwracać *prawdopodobieństwa* (Top 3) oraz można go łatwo douczać (`partial_fit` lub szybkie przetrenowanie całego małego zbioru).
  - Wybór: `MultinomialNB` (Najazd Bayes) lub bardzo prosty `SVC` z `probability=True`. Biorąc pod uwagę szybkość i mały zbiór punktowy, `MultinomialNB` lub szybkie wyliczenie podobieństwie cosinusowych (Cosine Similarity) na wektorach do zadania KNN będzie w 100% użyteczeną aproksymacją i natychmiastowym refitem.

## Strategia Architektoniczna

Ponieważ wolumen danych jest tak mały, najsensowniejszym podejściem z punktu widzenia projektowego będzie **retrening On-The-Fly**, polegający na pobraniu wszystkich wpisów historycznych (np. z ostatnich lat, chociaż przy 50-100 rekordach/miesiąc i 10 MB limitach to ułamek sekundy trwania trenowania) i wygenerowanie predykcji.

1.  **Zależności:** Dodanie `scikit-learn` opartego na `numpy/scipy/threadpoolctl` do `requirements.txt`.
2.  **Baza Danych:** Wyciągnięcie zgromadzonych historycznych faktur (`Invoice` + Linie z przypisanymi kontami `InvoiceLine`).
3.  **Implementacja ML:** Moduł `src/kontakt/ai/engine.py` eksponujący zaledwie funkcję pobrania wszystkich transakcji, zbudowania TF-IDF, wytrenowania lekkiego klasyfikatora dla unikalnych "kombinacji kont" i rzucenia odpowiedzi w postaci `Dict` (Top 3 z prawdopodobieństwami).

Zgodnie z modelem GSD, Faza 2 może zostać rozbita na dwie grupy zadań (Plany):
- Plan 1: Integracja ML + Warstwa dostępu / trenowania modeli (Backend).
- Plan 2: Podpięcie warstwy pod UI i wyświetlanie Top 3 sugestii dla użytkownika (Frontend/UI).
