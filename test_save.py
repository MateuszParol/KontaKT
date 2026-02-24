from kontakt.database.db import database
from kontakt.database.models import Document, DocumentLine, Account, Contractor
from datetime import date

try:
    database.connect()
    c, _ = Contractor.get_or_create(name="Test", defaults={'nip': "123"})
    a, _ = Account.get_or_create(symbol="101", defaults={'name': "Kasa"})
    
    doc = Document.create(
        document_type="Faktura",
        number="TEST/1",
        date_issue=str(date.today()),
        description="Test desc",
        amount=100.0,
        contractor_id=c.id
    )
    line = DocumentLine.create(
        document=doc,
        account_wn_id=a.id,
        account_ma_id=a.id,
        amount=100.0
    )
    print("SUCCESS")
except Exception as e:
    print(f"EXCEPTION: {e}")
