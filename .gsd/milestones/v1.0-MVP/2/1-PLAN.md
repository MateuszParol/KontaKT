---
phase: 2
plan: 1
wave: 1
depends_on: []
files_modified: ["requirements.txt", "src/kontakt/ai/engine.py"]
autonomous: true

must_haves:
  truths:
    - "Silnik AI potrafi zwrócić do 3 najbardziej prawdopodobnych propozycji dekretacji na podstawie opisu zdarzenia"
    - "Silnik opiera się o model scikit-learn i trenuje offline używając historii z bazy"
  artifacts:
    - "src/kontakt/ai/engine.py exists"
    - "Lista zależności w requirements.txt jest rozszerzona o scikit-learn"
  key_links:
    - "AI engine importuje bazę z z models.py by analizować historyczne faktury wraz z przypisanymi im kontami WN i MA"
---

# Plan 2.1: Model i Silnik Sztucznej Inteligencji (AI)

<objective>
Zintegrowanie frameworka Machine Learning (scikit-learn) z aplikacją, aby na podstawie opisu wprowadzanego w formularzu Faktur zwracać sugestie odpowiedniego dekretowania (paragraf, konto WN, konto MA) przy użyciu lokalnego analizowania offline.

Purpose: Niezależny, uczący się od podstaw engine to "mózg" wizji z SPEC.md, bez którego integracje inteligentne nie istnieją.
Output: Rozbudowane pakiety w środowisku. Napisany w pełni bezkontekstowy moduł `engine.py`, analizujący bazę danych SQLite.
</objective>

<context>
Load for context:
- .gsd/SPEC.md
- src/kontakt/database/models.py
- requirements.txt
</context>

<tasks>

<task type="auto">
  <name>Instalacja i konfiguracja frameworków ML</name>
  <files>requirements.txt</files>
  <action>
    Dodaj `scikit-learn` do wymagań `requirements.txt`.
    AVOID: Instalowania nadmiernych i ciężkich bibliotek jak Pytorch czy Tensorflow, ponieważ aplikacja musi być lekka, łatwa do uruchomienia na słabych maszynach w biurze.
  </action>
  <verify>grep "scikit-learn" requirements.txt</verify>
  <done>Plik konfiguracyjny z dependencies ma wskazany pakiet modelowy.</done>
</task>

<task type="auto">
  <name>Implementacja klasyfikatora ML</name>
  <files>src/kontakt/ai/engine.py</files>
  <action>
    Stwórz nowy moduł `src/kontakt/ai/engine.py`.
    Stwórz klasę `AIEngine`. Moduł docelowo ma eksponować dwie rzeczy: uczenie i predykcję powiązania `Invoice.description` -> kombinacji `[InvoiceLine.account_wn, InvoiceLine.account_ma]`.
    Mechanizm powinien pod spodem inicjować połączenie z bazą, iterować przez wszystkie opłacone/zweryfikowane linie i budować korpus TF-IDF (`TfidfVectorizer`). Następnie na tym korpusie uczyć `MultinomialNB`.
    Predykcja ma przyjmować `string` (nowy opis), przepuszczać go przy pomocy wyuczonego wczesniej ujętego w pamięci RAM `TfidfVectorizer`a, pobierać klasy prawdopodobieństwa od modelu `Predict_proba`, sortować listę po ufności top_n=3 i zwracać obiekty zawierające kombinacje dekretacji i % matchu.
    Gdy transakcji/historii całkowicie brakuje, metoda predykcji powinna zwracać predykcję typu pustego (fallback/empty array).
  </action>
  <verify>python -c "from kontakt.ai.engine import AIEngine"</verify>
  <done>Moduł silnika AI istnieje i zawiera podstawowy przepływ wirtualnego przewidywania na logice TF-IDF + NaiveBayes.</done>
</task>

</tasks>

<verification>
After all tasks, verify:
- [ ] Utworzenie modułu `engine.py` i pomyślny import scikit-learn.
- [ ] Funkcjonalne zmapowanie starych rekordów bazy na logikę macierzową tekstowo-decyzyjną.
</verification>

<success_criteria>
- [ ] All tasks verified
- [ ] Must-haves confirmed
</success_criteria>
