
from kontakt.database.db import database
from kontakt.database.models import Account, Contractor, Document, DocumentLine

def init_db():
    print("Inicjalizacja bazy danych...")
    database.connect(reuse_if_open=True)
    
    # Tworzenie tabel
    database.create_tables([Account, Contractor, Document, DocumentLine], safe=True)
    
    # Seed default accounts (Budget Units)
    default_accounts = [
        ("101", "Kasa", "Środki pieniężne w kasie"),
        ("130", "Rachunek bieżący jednostki", "Rachunek bankowy dochodów i wydatków"),
        ("201", "Rozrachunki z odbiorcami i dostawcami", "Ewidencja rozrachunków"),
        ("401", "Zużycie materiałów i energii", "Koszty podstawowe"),
        ("402", "Usługi obce", "Koszty usług"),
        ("800", "Fundusz jednostki", "Równowartość majątku trwałego")
    ]
    
    print("Tworzenie planu kont...")
    for symbol, name, desc in default_accounts:
        Account.get_or_create(symbol=symbol, defaults={'name': name, 'description': desc})
        
    print("Baza danych gotowa.")
    database.close()

if __name__ == "__main__":
    init_db()
