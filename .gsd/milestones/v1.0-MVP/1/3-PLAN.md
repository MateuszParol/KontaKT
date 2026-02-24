---
phase: 1
plan: 3
wave: 2
---

# Plan 1.3: UI Shell & Navigation

## Objective
Build the main application layout with Sidebar navigation and view switching mechanism.

## Context
- src/kontakt/main.py
- src/kontakt/ui/

## Tasks

<task type="auto">
  <name>Navigation Component</name>
  <files>src/kontakt/ui/views/sidebar.py</files>
  <action>
    Create a `Sidebar` class (inheriting `ctk.CTkFrame`) with buttons:
    - "Nowa Faktura"
    - "Historia"
    - "Kontrahenci"
    - "Plan Kont"
    - "Ustawienia"
    Each button should trigger a callback passed from the main App.
  </action>
  <verify>
    Check visual presence of buttons.
  </verify>
  <done>Sidebar displays correctly.</done>
</task>

<task type="auto">
  <name>View Manager</name>
  <files>src/kontakt/ui/app.py</files>
  <action>
    Refactor `main.py` entry point to use a robust `App` class in `src/kontakt/ui/app.py`.
    1. Layout: Grid 1x2 (Sidebar Left, Content Right).
    2. Function `show_view(view_name)` to clear right frame and load new view.
    3. Create basic Placeholder views for each section.
  </action>
  <verify>
    Run app and click sidebar buttons - content area should change text.
  </verify>
  <done>Navigation works smoothly.</done>
</task>

<task type="auto">
  <name>Invoice Input Form</name>
  <files>src/kontakt/ui/views/invoice_add.py</files>
  <action>
    Implement the "Nowa Faktura" view:
    - DateEntry (or Entry with validation).
    - Entry for "Numer Faktury".
    - ComboBox for "Kontrahent".
    - Textbox (large) for "Opis zdarzenia" (Critical for AI).
    - Entry for "Kwota".
    - "Zapisz" button (dummy logic for now).
  </action>
  <verify>
    Run app, navigate to "Nowa Faktura".
  </verify>
  <done>Form fields are visible and layout is clean.</done>
</task>

## Success Criteria
- [ ] Navigation switches views.
- [ ] Sidebar is persistent.
- [ ] Invoice Input form has all required fields for SPEC.
