
import customtkinter as ctk
from datetime import date
from kontakt.database.models import Contractor, Invoice

class InvoiceAddView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Header
        self.header = ctk.CTkLabel(self, text="Nowa Faktura", font=ctk.CTkFont(size=24, weight="bold"))
        self.header.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="w")
        
        # Form Fields
        
        # Numer Faktury
        self.lbl_number = ctk.CTkLabel(self, text="Numer Faktury:")
        self.lbl_number.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        self.entry_number = ctk.CTkEntry(self, placeholder_text="FV/2023/...")
        self.entry_number.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        # Data Wystawienia
        self.lbl_date = ctk.CTkLabel(self, text="Data Wystawienia (RRRR-MM-DD):")
        self.lbl_date.grid(row=1, column=1, padx=20, pady=5, sticky="w")
        self.entry_date = ctk.CTkEntry(self, placeholder_text=str(date.today()))
        self.entry_date.grid(row=2, column=1, padx=20, pady=5, sticky="ew")
        self.entry_date.insert(0, str(date.today()))

        # Kontrahent
        self.lbl_contractor = ctk.CTkLabel(self, text="Kontrahent:")
        self.lbl_contractor.grid(row=3, column=0, columnspan=2, padx=20, pady=5, sticky="w")
        
        self.contractors_map = {} # Name -> ID
        self.combo_contractor = ctk.CTkComboBox(self, values=[])
        self.combo_contractor.grid(row=4, column=0, columnspan=2, padx=20, pady=5, sticky="ew")
        self.refresh_contractors()

        # Opis
        self.lbl_desc = ctk.CTkLabel(self, text="Opis zdarzenia (dla AI):")
        self.lbl_desc.grid(row=5, column=0, columnspan=2, padx=20, pady=5, sticky="w")
        self.txt_desc = ctk.CTkTextbox(self, height=100)
        self.txt_desc.grid(row=6, column=0, columnspan=2, padx=20, pady=5, sticky="ew")

        # Kwota
        self.lbl_amount = ctk.CTkLabel(self, text="Kwota Brutto:")
        self.lbl_amount.grid(row=7, column=0, padx=20, pady=5, sticky="w")
        self.entry_amount = ctk.CTkEntry(self, placeholder_text="0.00")
        self.entry_amount.grid(row=8, column=0, padx=20, pady=5, sticky="ew")

        # Buttons
        self.btn_save = ctk.CTkButton(self, text="Zapisz i Dekretuj (AI)", fg_color="green", command=self.save_invoice)
        self.btn_save.grid(row=9, column=1, padx=20, pady=20, sticky="e")
        
        self.lbl_status = ctk.CTkLabel(self, text="")
        self.lbl_status.grid(row=9, column=0, padx=20, pady=20, sticky="w")

    def refresh_contractors(self):
        self.contractors_map = {}
        values = []
        for c in Contractor.select().order_by(Contractor.name):
            self.contractors_map[c.name] = c.id
            values.append(c.name)
        
        if not values:
            values = ["Brak kontrahentów - dodaj w zakładce Kontrahenci"]
            
        self.combo_contractor.configure(values=values)
        if values:
            self.combo_contractor.set(values[0])

    def save_invoice(self):
        number = self.entry_number.get()
        date_issue = self.entry_date.get()
        desc = self.txt_desc.get("1.0", "end-1c")
        amount = self.entry_amount.get()
        contractor_name = self.combo_contractor.get()
        
        contractor_id = self.contractors_map.get(contractor_name)
        
        if not all([number, date_issue, desc, amount, contractor_id]):
            self.lbl_status.configure(text="Błąd: Wypełnij wszystkie pola!", text_color="red")
            return

        try:
            Invoice.create(
                number=number,
                date_issue=date_issue,
                description=desc,
                amount=float(amount.replace(',', '.')),
                contractor_id=contractor_id
            )
            self.lbl_status.configure(text="Zapisano poprawnie!", text_color="green")
            # Clear form
            self.entry_number.delete(0, "end")
            self.txt_desc.delete("1.0", "end")
            self.entry_amount.delete(0, "end")
        except Exception as e:
            self.lbl_status.configure(text=f"Błąd zapisu: {e}", text_color="red")
