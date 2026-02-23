# SPEC.md — Specyfikacja Projektu

> **Status**: `FINALIZED`

## Wizja
Inteligentny asystent księgowego (aplikacja desktopowa) dla jednostek budżetowych (np. PCPR), który automatyzuje proces dekretacji faktur. Program działa w pełni offline, zapewniając bezpieczeństwo danych, i uczy się na bazie historycznych operacji, sugerując odpowiednie konta (WN/MA) oraz paragrafy na podstawie opisu faktury. Jest zaprojektowany z myślą o osobach nietechnicznych – intuicyjny, czytelny i prosty w obsłudze.

## Cele
1.  **Inteligentna Dekretacja**: System sugeruje konta księgowe i paragrafy na podstawie opisu zdarzenia gospodarczego z trafnością >90% po fazie nauki.
2.  **Prywatność (Offline First)**: Całe przetwarzanie danych odbywa się lokalnie na komputerze użytkownika. Żadne dane nie opuszczają urzędu.
3.  **Prostota Obsługi**: Interfejs typu "jedno okno", minimalizujący liczbę kliknięć niezbędnych do uzyskania wyniku.

## Poza Zakresem (Non-Goals) (Bez Integracji)
-   Automatyczne księgowanie w systemach zewnętrznych (Progman, Symfonia) – brak możliwości technicznych po stronie 3rd party.
-   Pełna księgowość (księgi rachunkowe, sprawozdania) – program służy tylko do *wspomagania decyzji*.
-   Chmura / Mobile – aplikacja tylko desktopowa (Windows).
-   OCR – program przetwarza tekst wpisany/skopiowany przez użytkownika, nie skanuje obrazów (w wersji 1.0).

## Użytkownicy
-   **Księgowa Jednostki Budżetowej**: Osoba merytoryczna, przyzwyczajona do standardowych programów księgowych, ceniąca szybkość i brak skomplikowanych opcji technicznych.

## Ograniczenia
-   **System Operacyjny**: Windows 10/11.
-   **Sprzęt**: Standardowe komputery biurowe (brak dedykowanych GPU do AI), co wymusza lekkie modele ML.
-   **Wolumen**: 50-100 dokumentów miesięcznie (mały zbiór treningowy, szybkie douczanie).

## Kryteria Sukcesu
- [ ] Zarządzanie planem kont jednostki (dodawanie/edycja).
- [ ] Czas wyświetlenia sugestii dekretacji < 1 sekunda.
- [ ] Możliwość ręcznej korekty sugestii, która "doucza" system.
- [ ] Intuicyjny interfejs (brak zgłoszeń o "niezrozumiałej funkcji" w testach).
- [ ] Działanie 100% offline (brak połączeń sieciowych).
