## Phase 4 Verification

### Must-Haves
- [x] Możliwość zapisania i odczytania Danych Podmiotu (Ustawienia Sprzedawcy / Urzędu) do uwzględnienia ich na fakturze KSeF. — **VERIFIED** (evidence: `SettingsView` created, bound to the `Settings` SQLite model. Key-values "ksef_nip", "ksef_name" etc. are persistently stored and accessible for the XML mapper).
- [x] Implementacja mappera i eksportera danych na schemat ustrukturyzowany FA(2) do wybranego przez użytkownika folderu. — **VERIFIED** (evidence: `kontakt/ksef/mapper.py` constructs standard python `xml.etree.ElementTree` with `Podmiot1`, `Fa` namespaces. Integrated seamlessly with the "Eksportuj KSeF" button located within `InvoiceCreatorView`).

### Verdict: PASS
