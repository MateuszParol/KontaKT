---
phase: 1
plan: 2
wave: 1
---

# Plan 1.2: Database & Models

## Objective
Implement the local SQLite database layer using Peewee ORM. Define models for Contractors, Invoices, and Chart of Accounts.

## Context
- .gsd/SPEC.md
- .gsd/phases/1/RESEARCH.md
- src/kontakt/config.py (created in 1.1)

## Tasks

<task type="auto">
  <name>Database Connection</name>
  <files>src/kontakt/database/db.py</files>
  <action>
    1. Implement a singleton database connection using `peewee.SqliteDatabase`.
    2. Use `config.USER_DATA_DIR` path for the SQLite file (`kontakt.db`).
    3. Ensure foreign keys support is enabled (`ragmas= {'foreign_keys': 1}`).
  </action>
  <verify>
    python -c "from src.kontakt.database.db import database; print(database.database)"
  </verify>
  <done>Database object initializes with correct path.</done>
</task>

<task type="auto">
  <name>Define Models</name>
  <files>src/kontakt/database/models.py</files>
  <action>
    Create Peewee models:
    1. `BaseModel`: inheriting from `peewee.Model` and linked to `db`.
    2. `Account` (Plan Kont): `symbol` (unique), `name`, `description`.
    3. `Contractor` (Kontrahent): `nip` (unique, optional), `name`, `address`.
    4. `Invoice` (Faktura): `number`, `date_issue`, `description`, `amount`, `contractor_id` (FK), `created_at`.
    5. `InvoiceLine` (Dekret): `invoice_id` (FK), `account_wn` (FK), `account_ma` (FK), `amount`.
  </action>
  <verify>
    Inspect file content for correct field types and relationships.
  </verify>
  <done>Models cover all entities from SPEC.</done>
</task>

<task type="auto">
  <name>Initialize Database Script</name>
  <files>src/kontakt/database/init_db.py</files>
  <action>
    Create a script to:
    1. Connect to DB.
    2. Create tables (`db.create_tables([...], safe=True)`).
    3. Seed default "Plan Kont" (standardowe konta budżetowe: 401, 402, 101, 130, 201).
  </action>
  <verify>
    python src/kontakt/database/init_db.py
  </verify>
  <done>Running script creates .db file and tables.</done>
</task>

## Success Criteria
- [ ] Models defined for core entities.
- [ ] Database file created in user data directory.
- [ ] Tables initialized successfully.
- [ ] Basic Chart of Accounts seeded.
