import os
import pandas as pd
from fpdf import FPDF
from kontakt.database.models import Document

def export_invoice_to_pdf(document_id: int, filepath: str) -> tuple[bool, str]:
    """Generuje Polecenie Księgowania do pliku PDF."""
    try:
        invoice = Document.get_by_id(document_id)
        
        pdf = FPDF()
        pdf.add_page()
        
        # Opcjonalnie załadowanie czcionki ze wsparciem polskich znaków,
        # jednak fpdf2 domyślnie wspiera standardowe 14 czcionek bez UTF-8, użyjmy 'helvetica' z ostrożnym kodowaniem lub fpdf2 wspiera domyślnie.
        # FPDF2 ma wbudowaną czcionkę helvetica ale dla polskich znaków lepiej dodać darmową.
        # W ramach uproszczenia, jeśli fpdf2 (nowsze) wspiera utf-8 na wbudowanych:
        pdf.set_font("helvetica", "B", 16)
        pdf.cell(0, 10, "POLECENIE KSIĘGOWANIA (PK)", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(10)
        
        pdf.set_font("helvetica", "", 12)
        pdf.cell(0, 8, f"Dokument źródłowy (Faktura): {invoice.number}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 8, f"Data wystawienia: {invoice.date_issue}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 8, f"Kontrahent: {invoice.contractor.name}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 8, f"NIP: {invoice.contractor.nip or 'Brak'}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 8, f"Kwota Brutto: {invoice.amount} PLN", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)
        
        pdf.set_font("helvetica", "I", 10)
        # Handle newlines in text for FPDF safely
        desc_clean = invoice.description.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 6, f"Opis operacji: {desc_clean}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(10)
        
        # Tabela dekretacji
        pdf.set_font("helvetica", "B", 11)
        pdf.cell(60, 8, "Konto WN", border=1, align="C")
        pdf.cell(60, 8, "Konto MA", border=1, align="C")
        pdf.cell(40, 8, "Kwota PLN", border=1, align="C", new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_font("helvetica", "", 11)
        for line in invoice.lines:
            pdf.cell(60, 8, str(line.account_wn.symbol), border=1, align="C")
            pdf.cell(60, 8, str(line.account_ma.symbol), border=1, align="C")
            pdf.cell(40, 8, str(line.amount), border=1, align="C", new_x="LMARGIN", new_y="NEXT")
            
        pdf.ln(20)
        pdf.cell(0, 8, ".......................................................", align="R", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 5, "Podpis Osob. Upoważnionej", align="R", new_x="LMARGIN", new_y="NEXT")
        
        pdf.output(filepath)
        return True, "Zapisano poprawnie"
    except Exception as e:
        return False, f"Błąd PDF: {str(e)}"

def export_journal_to_excel(filepath: str) -> tuple[bool, str]:
    """Generuje zestawienie (Dziennik Księgowań) do Excela .xlsx ."""
    try:
        data = []
        for invoice in Document.select().order_by(Document.date_issue.desc()):
            for line in invoice.lines:
                data.append({
                    "Dokument": invoice.number,
                    "Data": invoice.date_issue,
                    "Kontrahent": invoice.contractor.name,
                    "Opis": invoice.description,
                    "Konto WN": line.account_wn.symbol,
                    "Konto MA": line.account_ma.symbol,
                    "Kwota": float(line.amount)
                })
        
        if not data:
            return False, "Brak operacji do wyeksportowania."
            
        df = pd.DataFrame(data)
        df.to_excel(filepath, engine="openpyxl", index=False)
        return True, "Zapisano Dziennik poprawnie"
    except Exception as e:
        return False, f"Błąd Excel: {str(e)}"
