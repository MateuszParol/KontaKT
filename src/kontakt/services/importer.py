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

def import_contractors_from_excel(filepath: str) -> tuple[int, str]:
    """
    Czyta plik Excel i ładuje go do tabeli Contractor.
    Mapuje pola takie jak Pełna nazwa, REGON/PESEL, NIP, Miejscowość, Ulica, Kod Pocztowy -> Contractor(nip, name, address).
    """
    try:
        from kontakt.database.models import Contractor
        
        engine = 'xlrd' if filepath.lower().endswith('.xls') else 'openpyxl'
        df = pd.read_excel(filepath, engine=engine)
        
        # Weryfikacja niezbędnych kolumn by stwierdzić, że to nie jest zupełnie zły plik
        if 'Pełna nazwa' not in df.columns and 'Nazwa skrócona' not in df.columns:
            return 0, "Błąd: Brak kolumn z nazwą kontrahenta w pliku."
            
        added_count = 0
        updated_count = 0
        
        for index, row in df.iterrows():
            # Nazwa -> Priorytet na pełną nazwą, zapas to skrócona
            name = str(row.get('Pełna nazwa', '')).strip()
            if not name or name.lower() == 'nan':
                 name = str(row.get('Nazwa skrócona', '')).strip()
                 
            if not name or name.lower() == 'nan':
                 continue  # Bez nazwy ignorujemy wiersz

            # NIP
            nip = str(row.get('NIP', '')).replace('-', '').strip()
            if nip.lower() == 'nan' or not nip:
                 nip = None # Peewee null
                 
            # Adres sklejony - Oczekuje rozdzielenia (Ulica, Kod Miejscowość)
            ulica = str(row.get('Ulica', '')).strip()
            kod = str(row.get('Kod pocztowy', '')).strip()
            miejscowosc = str(row.get('Miejscowość', '')).strip()
            
            parts = []
            if ulica and ulica.lower() != 'nan': parts.append(ulica)
            
            # Sub-łączenie dla kodu i miejscowosci np "00-111 Warszawa"
            miasto_parts = []
            if kod and kod.lower() != 'nan': miasto_parts.append(kod)
            if miejscowosc and miejscowosc.lower() != 'nan': miasto_parts.append(miejscowosc)
            
            if miasto_parts:
                 parts.append(" ".join(miasto_parts))
                 
            final_address = ", ".join(parts) if parts else None
                 
            # Zasilenie do DB (Peewee get_or_create na podstawie unikatowanego NIPu ORAZ / LUB nazwy w razie braku). U nas w modelu unikalności twardej na db nie nałożyliśmy ale przyjmijmy name.
            # Jeśli get_or_create napotka get bo już był wpis -> nie ma problemu.
            try:
                if nip:
                    contractor, created = Contractor.get_or_create(
                        nip=nip,
                        defaults={'name': name, 'address': final_address}
                    )
                else:
                    contractor, created = Contractor.get_or_create(
                        name=name,
                        defaults={'nip': None, 'address': final_address}
                    )
                
                if created:
                    added_count += 1
                else:
                    # Update awaryjny (np adres)
                    updated = False
                    if contractor.address != final_address:
                        contractor.address = final_address
                        updated = True
                    if contractor.name != name:
                        contractor.name = name
                        updated = True
                        
                    if updated:
                        contractor.save()
                        updated_count += 1
                        
            except IntegrityError:
                continue

        return added_count, f"Dodano {added_count} nowych kontrahentów. (Zaktualizowano {updated_count})"

    except Exception as e:
        return 0, f"Błąd Importu: {str(e)}"
