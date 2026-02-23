---
phase: 1
plan: 4
wave: 3
---

# Plan 1.4: Data Management UI

## Objective
Implement the UI for managing "Plan Kont" (Chart of Accounts) and "Kontrahenci" (Contractors), and integrate the Invoice Form with the database.

## Context
- src/kontakt/ui/views/sidebar.py
- src/kontakt/ui/app.py
- src/kontakt/database/models.py

## Tasks

<task type="auto">
  <name>Accounts View</name>
  <files>src/kontakt/ui/views/accounts.py</files>
  <action>
    Implement `AccountsView` class:
    1. List existing accounts (Symbol, Name) in a ScrollableFrame or Textbox (read-only list).
    2. Form to add new account (Symbol, Name, Description) + "Dodaj" button.
    3. On "Dodaj", save to DB (`Account.create`) and refresh list.
  </action>
  <verify>
    Run app, go to "Plan Kont", add a test account, see it appear.
  </verify>
  <done>Can add and view accounts.</done>
</task>

<task type="auto">
  <name>Contractors View</name>
  <files>src/kontakt/ui/views/contractors.py</files>
  <action>
    Implement `ContractorsView` class:
    1. List existing contractors.
    2. Form to add new contractor (NIP, Name, Address).
    3. Save to DB.
  </action>
  <verify>
    Run app, go to "Kontrahenci" (update App routing first), add contractor.
  </verify>
  <done>Can add and view contractors.</done>
</task>

<task type="auto">
  <name>Integrate Invoice Form</name>
  <files>src/kontakt/ui/views/invoice_add.py, src/kontakt/ui/app.py</files>
  <action>
    1. Update `InvoiceAddView`:
       - Fetch contractors from DB (`Contractor.select()`) to populate `combo_contractor`.
       - Implement `save_invoice` to create `Invoice` record in DB.
    2. Update `App.show_view` to handle "accounts" and "contractors" routes.
  </action>
  <verify>
    Run app, see contractors in dropdown, save invoice, check DB or console log.
  </verify>
  <done>Invoice form is connected to DB.</done>
</task>

## Success Criteria
- [ ] Working "Plan Kont" management.
- [ ] Working "Kontrahenci" management.
- [ ] Invoice form saves data to SQLite.
