import xml.etree.ElementTree as ET
from datetime import datetime
from kontakt.database.models import SalesInvoice, SalesInvoiceItem, Settings

class KsefMapper:
    @staticmethod
    def generate_xml(invoice_id, filepath):
        # 1. Pobierz dane
        try:
            invoice = SalesInvoice.get_by_id(invoice_id)
        except SalesInvoice.DoesNotExist:
            raise Exception("Taka faktura nie istnieje w bazie.")
            
        settings_dict = {s.key: s.value for s in Settings.select()}
        my_nip = settings_dict.get("ksef_nip", "").replace("-", "").replace(" ", "")
        my_name = settings_dict.get("ksef_name", "")
        
        if not my_nip or not my_name:
            raise Exception("Brak danych Twojego Urzędu (NIP/Nazwa). Uzupełnij je w zakładce Ustawienia.")

        nabywca_nip = (invoice.contractor.nip or "").replace("-", "").replace(" ", "")
        nabywca_nazwa = invoice.contractor.name
        nabywca_adres = invoice.contractor.address or "Brak adresu"

        # 2. Namespace KSeF (FA 2)
        NS = "http://crd.gov.pl/wzor/2023/06/29/12648/"
        ET.register_namespace('', NS)
        
        # 3. Budujemy Drzewo
        root = ET.Element(f"{{{NS}}}Faktura")
        
        # Naglowek
        naglowek = ET.SubElement(root, f"{{{NS}}}Naglowek")
        kod_formularza = ET.SubElement(naglowek, f"{{{NS}}}KodFormularza", kodSystemowy="FA (2)", wersjaSchemy="1-0E")
        kod_formularza.text = "FA"
        wariant_formularza = ET.SubElement(naglowek, f"{{{NS}}}WariantFormularza")
        wariant_formularza.text = "2"
        data_wytworzenia = ET.SubElement(naglowek, f"{{{NS}}}DataWytworzeniaFa")
        data_wytworzenia.text = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

        # Rozdzielczość 
        # Podmiot1 (Sprzedawca)
        podmiot1 = ET.SubElement(root, f"{{{NS}}}Podmiot1")
        dane_identyfikacyjne1 = ET.SubElement(podmiot1, f"{{{NS}}}DaneIdentyfikacyjne")
        ET.SubElement(dane_identyfikacyjne1, f"{{{NS}}}NIP").text = my_nip
        ET.SubElement(dane_identyfikacyjne1, f"{{{NS}}}Nazwa").text = my_name

        # Podmiot2 (Nabywca)
        podmiot2 = ET.SubElement(root, f"{{{NS}}}Podmiot2")
        dane_identyfikacyjne2 = ET.SubElement(podmiot2, f"{{{NS}}}DaneIdentyfikacyjne")
        if nabywca_nip:
            ET.SubElement(dane_identyfikacyjne2, f"{{{NS}}}NIP").text = nabywca_nip
        else:
            ET.SubElement(dane_identyfikacyjne2, f"{{{NS}}}BrakID").text = "1"
        ET.SubElement(dane_identyfikacyjne2, f"{{{NS}}}Nazwa").text = nabywca_nazwa

        # Sekcja Fa
        fa = ET.SubElement(root, f"{{{NS}}}Fa")
        ET.SubElement(fa, f"{{{NS}}}KodWaluty").text = "PLN"
        ET.SubElement(fa, f"{{{NS}}}P_1").text = invoice.date_issue.strftime("%Y-%m-%d") # Data wystawienia
        ET.SubElement(fa, f"{{{NS}}}P_2").text = invoice.number # Numer FA
        ET.SubElement(fa, f"{{{NS}}}P_6").text = invoice.date_sale.strftime("%Y-%m-%d") # Data sprzedaży
        
        # Podsumowania wstepne (Wymagane przez sceme Fa)
        sum_netto = sum(item.total_net for item in invoice.items)
        sum_brutto = sum(item.total_gross for item in invoice.items)
        ET.SubElement(fa, f"{{{NS}}}P_13_1").text = f"{sum_netto:.2f}" # Suma netto
        ET.SubElement(fa, f"{{{NS}}}P_15").text = f"{sum_brutto:.2f}" # Suma brutto
        ET.SubElement(fa, f"{{{NS}}}P_16").text = "0" # Zaplacono? w tej implementacji nie wnikamy
        
        # Sekcja pozycje - P_26 (Itemy)
        for i, item in enumerate(invoice.items, start=1):
            wiersz = ET.SubElement(fa, f"{{{NS}}}FaWiersz")
            ET.SubElement(wiersz, f"{{{NS}}}NrWierszaFa").text = str(i)
            ET.SubElement(wiersz, f"{{{NS}}}P_7").text = item.product_name
            ET.SubElement(wiersz, f"{{{NS}}}P_8A").text = "szt" # w uproszczeniu
            ET.SubElement(wiersz, f"{{{NS}}}P_8B").text = f"{item.quantity:.2f}"
            ET.SubElement(wiersz, f"{{{NS}}}P_9A").text = f"{item.price_net:.2f}"
            ET.SubElement(wiersz, f"{{{NS}}}P_11").text = f"{item.total_net:.2f}"
            ET.SubElement(wiersz, f"{{{NS}}}P_12").text = str(item.vat_rate) 

        # 4. Zapis do pliku
        tree = ET.ElementTree(root)
        try:
            # Domyslnie KSeF wymaga kodowania UTF-8 i deklaracji XML
            tree.write(filepath, encoding="utf-8", xml_declaration=True)
        except Exception as e:
            raise Exception(f"Błąd podczas zapisu pliku: {e}")
