import pandas as pd
from kontakt.database.models import Account
from peewee import IntegrityError

def import_accounts_from_excel(filepath: str) -> tuple[int, str]:
    """
    Czyta pożądany plik Excel i ładuje go do tabeli Account.
    Wspiera stare pliki .xls używając xlrd i .xlsx dla kompatybilności.
    """
    try:
        # Determine engine based on extension
        engine = 'xlrd' if filepath.lower().endswith('.xls') else 'openpyxl'
        
        # Oczekiwane kolumny: WY_KONTO, WY_NAZWA, KONTO
        df = pd.read_excel(filepath, engine=engine)
        
        # Weryfikacja wymaganych kolumn (KONTO i WY_NAZWA są minimum egzystyncjalnym)
        required_columns = ['KONTO', 'WY_NAZWA']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return 0, f"Błąd: W pliku brakuje kolumn: {', '.join(missing_columns)}"
            
        # Oczyszczanie Danych (Dropna tam gdzie brak nr konta)
        df_clean = df.dropna(subset=['KONTO'])
        
        added_count = 0
        updated_count = 0
        
        for index, row in df_clean.iterrows():
            # Ensure types are string, strip whitespace
            symbol = str(row['KONTO']).strip()
            name = str(row.get('WY_NAZWA', '')).strip()
            
            if not symbol or symbol.lower() == 'nan':
                 continue
                 
            # Peewee get_or_create
            account, created = Account.get_or_create(
                symbol=symbol,
                defaults={'name': name}
            )
            
            if created:
                added_count += 1
            else:
                # Jeśli z jakiegoś powodu nazwa w pliku jest inna i chcemy zaktualizować (Opcjonalnie)
                if account.name != name:
                    account.name = name
                    account.save()
                    updated_count += 1

        return added_count, f"Import Zakończony: Dodano {added_count} nowych kont. (Zaktualizowano {updated_count})"

    except Exception as e:
        return 0, f"Błąd Importu: {str(e)}"
