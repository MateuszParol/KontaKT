# Phase 4 Research

- **UI Performance**: CustomTkinter lists can become slow with thousands of items. Using Peewee `.limit(100)` restricts query sizes and prevents UI freezing. The existing search fields can trigger bounded queries.
- **Excel Import**: Python environment has `pandas`, `xlrd`, and `openpyxl` which support reading both legacy and modern Excel files. The contractor data (NIP, REGON, Adres, Nazwa) can be mapped correctly to the `Contractor(nip, name, address)` model.
- **Current Standpoint**: During codebase mapping, it was discovered that elements of Phase 4 (limits, UI search, importer service) might already be present in code but not verified or marked complete in the ROADMAP. This plan will task the executor with verifying and finalizing the implementation.
