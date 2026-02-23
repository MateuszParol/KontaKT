import threading
import customtkinter as ctk
from datetime import date
from kontakt.database.models import Contractor, Invoice, Account, InvoiceLine

class InvoiceAddView(ctk.CTkFrame):
    def __init__(self, master, ai_engine=None):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.ai_engine = ai_engine
        
        self.grid_columnconfigure(0, weight=6)  # Formularz
        self.grid_columnconfigure(1, weight=4)  # Sugestie AI
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.header = ctk.CTkLabel(self, text="Nowa Faktura", font=ctk.CTkFont(size=24, weight="bold"))
        self.header.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="w")
        
        # ==== Form Frame ====
        self.form_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.form_frame.grid(row=1, column=0, sticky="nsew", padx=(20,10))
        
        # Numer Faktury
        self.lbl_number = ctk.CTkLabel(self.form_frame, text="Numer Faktury:")
        self.lbl_number.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_number = ctk.CTkEntry(self.form_frame, placeholder_text="FV/2023/...")
        self.entry_number.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # Data Wystawienia
        self.lbl_date = ctk.CTkLabel(self.form_frame, text="Data Wystawienia (RRRR-MM-DD):")
        self.lbl_date.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.entry_date = ctk.CTkEntry(self.form_frame, placeholder_text=str(date.today()))
        self.entry_date.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.entry_date.insert(0, str(date.today()))

        # Kontrahent
        self.lbl_contractor = ctk.CTkLabel(self.form_frame, text="Kontrahent:")
        self.lbl_contractor.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        
        self.contractors_map = {} 
        self.combo_contractor = ctk.CTkComboBox(self.form_frame, values=[])
        self.combo_contractor.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.refresh_contractors()

        # Opis
        self.lbl_desc = ctk.CTkLabel(self.form_frame, text="Opis zdarzenia (dla AI):")
        self.lbl_desc.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        self.txt_desc = ctk.CTkTextbox(self.form_frame, height=100)
        self.txt_desc.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # AI Trigger po utracie ostrości okna opisu
        self.txt_desc.bind("<FocusOut>", self.request_ai_suggestions)

        # Kwota
        self.lbl_amount = ctk.CTkLabel(self.form_frame, text="Kwota Brutto:")
        self.lbl_amount.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.entry_amount = ctk.CTkEntry(self.form_frame, placeholder_text="0.00")
        self.entry_amount.grid(row=7, column=0, padx=5, pady=5, sticky="ew")

        # Konta (WN, MA)
        self.lbl_accounts = ctk.CTkLabel(self.form_frame, text="Dekretacja (Konto WN / Konto MA):")
        self.lbl_accounts.grid(row=8, column=0, columnspan=2, pady=(20,0), sticky="w")
        
        self.accounts_map = {} # Display string -> ID
        self.accounts_id_to_symbol = {}
        
        self.combo_wn = ctk.CTkComboBox(self.form_frame, values=["Wybierz Konto WN"])
        self.combo_wn.grid(row=9, column=0, pady=5, sticky="ew", padx=(0,5))
        
        self.combo_ma = ctk.CTkComboBox(self.form_frame, values=["Wybierz Konto MA"])
        self.combo_ma.grid(row=9, column=1, pady=5, sticky="ew", padx=(5,0))
        
        self.refresh_accounts()

        # Buttons
        self.btn_save = ctk.CTkButton(self.form_frame, text="Zapisz Fakturę", fg_color="green", command=self.save_invoice)
        self.btn_save.grid(row=10, column=1, padx=5, pady=20, sticky="e")
        
        self.lbl_status = ctk.CTkLabel(self.form_frame, text="")
        self.lbl_status.grid(row=10, column=0, padx=5, pady=20, sticky="w")


        # ==== AI Suggestions Frame ====
        self.ai_frame = ctk.CTkFrame(self)
        self.ai_frame.grid(row=1, column=1, sticky="nsew", padx=(10,20), pady=(0, 20))
        
        self.ai_lbl = ctk.CTkLabel(self.ai_frame, text="✨ Sugestie AI", font=ctk.CTkFont(weight="bold", size=16))
        self.ai_lbl.pack(pady=15)
        
        self.ai_content = ctk.CTkFrame(self.ai_frame, fg_color="transparent")
        self.ai_content.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.show_ai_placeholder()

    def show_ai_placeholder(self, text="Wprowadź opis i odznacz pole,\naby otrzymać sugestie dektretacji."):
        for widget in self.ai_content.winfo_children():
            widget.destroy()
        lbl = ctk.CTkLabel(self.ai_content, text=text, text_color="gray")
        lbl.pack(pady=20)

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

    def refresh_accounts(self):
        self.accounts_map = {}
        self.accounts_id_to_symbol = {}
        values = []
        for a in Account.select().order_by(Account.symbol):
            display = f"{a.symbol} - {a.name}"
            self.accounts_map[display] = a.id
            self.accounts_id_to_symbol[a.id] = display
            values.append(display)
            
        if not values:
            values = ["Brak kont"]
            
        self.combo_wn.configure(values=values)
        self.combo_ma.configure(values=values)
        if values:
            self.combo_wn.set(values[0])
            self.combo_ma.set(values[0])

    def request_ai_suggestions(self, event=None):
        if not self.ai_engine:
            return
        
        desc = self.txt_desc.get("1.0", "end-1c").strip()
        if len(desc) < 3:
            return
            
        self.show_ai_placeholder("Analizuję...")
        
        def run_predict():
            results = self.ai_engine.predict(desc, top_n=3)
            # Update UI on main thread
            self.after(0, self.display_ai_suggestions, results)

        threading.Thread(target=run_predict, daemon=True).start()

    def display_ai_suggestions(self, results):
        for widget in self.ai_content.winfo_children():
            widget.destroy()
            
        if not results:
            self.show_ai_placeholder("Brak wystarczających historii\ndo zasugerowania dekretacji.")
            return
            
        for idx, res in enumerate(results):
            wn_display = self.accounts_id_to_symbol.get(res["account_wn_id"], "Nieznane")
            ma_display = self.accounts_id_to_symbol.get(res["account_ma_id"], "Nieznane")
            match = res["match_percent"]
            
            f = ctk.CTkFrame(self.ai_content)
            f.pack(fill="x", pady=5)
            
            text = f"WN: {wn_display}\nMA: {ma_display}\nPewność: {match}%"
            lbl = ctk.CTkLabel(f, text=text, justify="left", font=ctk.CTkFont(size=12))
            lbl.pack(side="left", padx=10, pady=5)
            
            # Apply suggestion button
            btn = ctk.CTkButton(f, text="Wybierz", width=60, height=24,
                                command=lambda w=wn_display, m=ma_display: self.apply_ai_suggestion(w, m))
            btn.pack(side="right", padx=10, pady=10)
            
            # Auto-select if confident and it's the first result
            if idx == 0 and match > 80.0:
                self.apply_ai_suggestion(wn_display, ma_display)
                
    def apply_ai_suggestion(self, wn_display, ma_display):
        self.combo_wn.set(wn_display)
        self.combo_ma.set(ma_display)

    def save_invoice(self):
        number = self.entry_number.get()
        date_issue = self.entry_date.get()
        desc = self.txt_desc.get("1.0", "end-1c").strip()
        amount = self.entry_amount.get()
        contractor_name = self.combo_contractor.get()
        
        wn_val = self.combo_wn.get()
        ma_val = self.combo_ma.get()
        
        contractor_id = self.contractors_map.get(contractor_name)
        wn_id = self.accounts_map.get(wn_val)
        ma_id = self.accounts_map.get(ma_val)
        
        if not all([number, date_issue, desc, amount, contractor_id, wn_id, ma_id]):
            self.lbl_status.configure(text="Błąd: Wypełnij wszystkie pola w tym konta!", text_color="red")
            return

        try:
            # Tworzymy fakturę
            invoice = Invoice.create(
                number=number,
                date_issue=date_issue,
                description=desc,
                amount=float(amount.replace(',', '.')),
                contractor_id=contractor_id
            )
            
            # Tworzymy linię dekretacyjną (to ona jest uzywana do nauki AI)
            InvoiceLine.create(
                invoice=invoice,
                account_wn_id=wn_id,
                account_ma_id=ma_id,
                amount=float(amount.replace(',', '.'))
            )
            
            self.lbl_status.configure(text="Zapisano poprawnie!", text_color="green")
            
            # Doucz model "na żywo" na podstawie nowo wprowadzonego rekordu
            if self.ai_engine:
                threading.Thread(target=self.ai_engine.train, daemon=True).start()
                
            # Czyszczenie forma
            self.entry_number.delete(0, "end")
            self.txt_desc.delete("1.0", "end")
            self.entry_amount.delete(0, "end")
            self.show_ai_placeholder()
            
        except Exception as e:
            self.lbl_status.configure(text=f"Błąd zapisu: {e}", text_color="red")
