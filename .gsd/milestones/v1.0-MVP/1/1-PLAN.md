---
phase: 1
plan: 1
wave: 1
---

# Plan 1.1: Project Skeleton & Environment

## Objective
Initialize the robust "src-layout" project structure, configure the Python environment, and verify the GUI framework (CustomTkinter) works.

## Context
- .gsd/SPEC.md
- .gsd/phases/1/RESEARCH.md

## Tasks

<task type="auto">
  <name>Initialize Environment</name>
  <files>.gitignore, requirements.txt</files>
  <action>
    1. Create `.gitignore` tailored for Python (venv, __pycache__, .db, .idea, etc.).
    2. Create `requirements.txt` with core dependencies: `customtkinter`, `peewee`, `pillow`, `platformdirs`, `packaging`.
  </action>
  <verify>
    Test-Path .gitignore; Test-Path requirements.txt
  </verify>
  <done>Files exist with correct content.</done>
</task>

<task type="auto">
  <name>Create Project Structure</name>
  <files>src/kontakt/__init__.py, src/kontakt/main.py, src/kontakt/config.py</files>
  <action>
    1. Create directory structure: `src/kontakt/ui`, `src/kontakt/database`, `src/kontakt/services`, `assets`, `data`, `tests`.
    2. Create `src/kontakt/__init__.py`.
    3. Create `config.py` using `platformdirs` to define `USER_DATA_DIR` (for database storage) and ensures the directory exists.
  </action>
  <verify>
    Test-Path src/kontakt/ui; Test-Path src/kontakt/main.py
  </verify>
  <done>Directory structure matches RESEARCH.md.</done>
</task>

<task type="auto">
  <name>Hello World GUI</name>
  <files>src/kontakt/main.py</files>
  <action>
    Implement a minimal `main.py` that:
    1. Imports `customtkinter`.
    2. Sets theme to "Dark".
    3. Displays a window titled "KontaKT" with size 1200x800.
    4. Shows a label "System Inicjalizacji...".
  </action>
  <verify>
    python src/kontakt/main.py
  </verify>
  <done>App window launches without errors.</done>
</task>

## Success Criteria
- [ ] Project structure created.
- [ ] Dependencies listed.
- [ ] `config.py` correctly resolves data paths on Windows.
- [ ] Application launches and shows a graphical window.
