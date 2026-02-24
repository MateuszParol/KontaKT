import threading
import customtkinter as ctk
from datetime import date
from kontakt.database.models import Contractor, Document, Account, DocumentLine
from kontakt.ui.components.selection_modal import SelectionModal

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
        
        self.contractor_id = None
        self.btn_contractor = ctk.CTkButton(self.form_frame, text="Wybierz Kontrahenta", fg_color="transparent", border_width=1, text_color=("gray10", "gray90"), anchor="w", command=self.open_contractor_modal)
        self.btn_contractor.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

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
        
        self.account_wn_id = None
        self.account_ma_id = None
        
        self.btn_wn = ctk.CTkButton(self.form_frame, text="Wybierz Konto WN", fg_color="transparent", border_width=1, text_color=("gray10", "gray90"), anchor="w", command=lambda: self.open_account_modal("wn"))
        self.btn_wn.grid(row=9, column=0, pady=5, sticky="ew", padx=(0,5))
        
        self.btn_ma = ctk.CTkButton(self.form_frame, text="Wybierz Konto MA", fg_color="transparent", border_width=1, text_color=("gray10", "gray90"), anchor="w", command=lambda: self.open_account_modal("ma"))
        self.btn_ma.grid(row=9, column=1, pady=5, sticky="ew", padx=(5,0))

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

    def open_contractor_modal(self):
        def fetch_contractors(phrase):
            query = Contractor.select()
            if phrase:
                query = query.where(Contractor.name.contains(phrase) | Contractor.nip.contains(phrase))
            return [(c.id, c.nip or "-", c.name) for c in query.order_by(Contractor.name)]
            
        def on_select(values):
            self.contractor_id = int(values[0])
            self.btn_contractor.configure(text=values[2])
            
        SelectionModal(
            self,
            title="Wybierz Kontrahenta",
            columns=[("id", "ID", 0), ("nip", "NIP", 100), ("name", "Nazwa", 400)],
            data_fetcher=fetch_contractors,
            on_select=on_select
        )

    def open_account_modal(self, acc_type):
        def fetch_accounts(phrase):
            query = Account.select()
            if phrase:
                query = query.where(Account.name.contains(phrase) | Account.symbol.contains(phrase))
            return [(a.id, a.symbol, a.name) for a in query.order_by(Account.symbol)]
            
        def on_select(values):
            if acc_type == "wn":
                self.account_wn_id = int(values[0])
                self.btn_wn.configure(text=f"{values[1]} - {values[2]}")
            else:
                self.account_ma_id = int(values[0])
                self.btn_ma.configure(text=f"{values[1]} - {values[2]}")
                
        SelectionModal(
            self,
            title=f"Wybierz Konto {'WN' if acc_type == 'wn' else 'MA'}",
            columns=[("id", "ID", 0), ("symbol", "Symbol", 100), ("name", "Nazwa", 400)],
            data_fetcher=fetch_accounts,
            on_select=on_select
        )

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
            wn_account = Account.get_or_none(Account.id == res["account_wn_id"])
            ma_account = Account.get_or_none(Account.id == res["account_ma_id"])
            
            wn_display = f"{wn_account.symbol} - {wn_account.name}" if wn_account else "Nieznane"
            ma_display = f"{ma_account.symbol} - {ma_account.name}" if ma_account else "Nieznane"
            match = res["match_percent"]
            
            # Use IDs for applying the suggestion
            wn_id = res["account_wn_id"]
            ma_id = res["account_ma_id"]
            
            f = ctk.CTkFrame(self.ai_content)
            f.pack(fill="x", pady=5)
            
            text = f"WN: {wn_display}\nMA: {ma_display}\nPewność: {match}%"
            lbl = ctk.CTkLabel(f, text=text, justify="left", font=ctk.CTkFont(size=12))
            lbl.pack(side="left", padx=10, pady=5)
            
            # Apply suggestion button
            btn = ctk.CTkButton(f, text="Wybierz", width=60, height=24,
                                command=lambda w_id=wn_id, m_id=ma_id, w_disp=wn_display, m_disp=ma_display: self.apply_ai_suggestion(w_id, m_id, w_disp, m_disp))
            btn.pack(side="right", padx=10, pady=10)
            
            # Auto-select if confident and it's the first result
            if idx == 0 and match > 80.0:
                self.apply_ai_suggestion(wn_id, ma_id, wn_display, ma_display)
                
    def apply_ai_suggestion(self, wn_id, ma_id, wn_display, ma_display):
        self.account_wn_id = wn_id
        self.account_ma_id = ma_id
        self.btn_wn.configure(text=wn_display)
        self.btn_ma.configure(text=ma_display)

    def save_invoice(self):
        number = self.entry_number.get()
        date_issue = self.entry_date.get()
        desc = self.txt_desc.get("1.0", "end-1c").strip()
        amount = self.entry_amount.get()
        contractor_id = self.contractor_id
        wn_id = self.account_wn_id
        ma_id = self.account_ma_id
        
        if not all([number, date_issue, desc, amount, contractor_id, wn_id, ma_id]):
            self.lbl_status.configure(text="Błąd: Wypełnij wszystkie pola w tym konta!", text_color="red")
            return

        try:
            # Tworzymy fakturę
            document = Document.create(
                document_type="Faktura",
                number=number,
                date_issue=date_issue,
                description=desc,
                amount=float(amount.replace(',', '.')),
                contractor_id=contractor_id
            )
            
            # Tworzymy linię dekretacyjną (to ona jest uzywana do nauki AI)
            DocumentLine.create(
                document=document,
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
            self.contractor_id = None
            self.btn_contractor.configure(text="Wybierz Kontrahenta")
            self.account_wn_id = None
            self.btn_wn.configure(text="Wybierz Konto WN")
            self.account_ma_id = None
            self.btn_ma.configure(text="Wybierz Konto MA")
            self.show_ai_placeholder()
            
        except Exception as e:
            self.lbl_status.configure(text=f"Błąd zapisu: {e}", text_color="red")
