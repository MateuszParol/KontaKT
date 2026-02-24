import threading
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from datetime import date
from kontakt.database.models import Contractor, Document, Account, DocumentLine
from kontakt.ui.components.selection_modal import SelectionModal

class DocumentAddView(ctk.CTkFrame):
    def __init__(self, master, ai_engine=None):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.ai_engine = ai_engine
        
        self.grid_columnconfigure(0, weight=6)  # Formularz
        self.grid_columnconfigure(1, weight=4)  # Sugestie AI
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.header = ctk.CTkLabel(self, text="Nowy Dokument", font=ctk.CTkFont(size=24, weight="bold"))
        self.header.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="w")
        
        # ==== Form Frame ====
        self.form_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.form_frame.grid(row=1, column=0, sticky="nsew", padx=(20,10))
        
        # Typ Dokumentu
        self.lbl_type = ctk.CTkLabel(self.form_frame, text="Typ Dokumentu:")
        self.lbl_type.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.combo_type = ctk.CTkComboBox(self.form_frame, values=["Faktura", "Wyciąg", "Nota"], state="readonly")
        self.combo_type.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.combo_type.set("Faktura")

        # Numer Dokumentu
        self.lbl_number = ctk.CTkLabel(self.form_frame, text="Numer Dokumentu:")
        self.lbl_number.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.entry_number = ctk.CTkEntry(self.form_frame, placeholder_text="FV/2023/...")
        self.entry_number.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Data Wystawienia
        self.lbl_date = ctk.CTkLabel(self.form_frame, text="Data Wystawienia (RRRR-MM-DD):")
        self.lbl_date.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_date = ctk.CTkEntry(self.form_frame, placeholder_text=str(date.today()))
        self.entry_date.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        self.entry_date.insert(0, str(date.today()))

        # Kontrahent
        self.lbl_contractor = ctk.CTkLabel(self.form_frame, text="Kontrahent:")
        self.lbl_contractor.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        self.contractor_id = None
        self.btn_contractor = ctk.CTkButton(self.form_frame, text="Wybierz Kontrahenta", fg_color="transparent", border_width=1, text_color=("gray10", "gray90"), anchor="w", command=self.open_contractor_modal)
        self.btn_contractor.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

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

        # Recent accounts memory frames
        self.recent_wn_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.recent_wn_frame.grid(row=10, column=0, pady=2, sticky="ew", padx=(0,5))
        
        self.recent_ma_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.recent_ma_frame.grid(row=10, column=1, pady=2, sticky="ew", padx=(5,0))

        self.load_recent_accounts()
        
        # Add / Clone Line Buttons
        self.btn_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.btn_frame.grid(row=11, column=0, columnspan=2, pady=(10,5), sticky="e")
        
        self.btn_add_line = ctk.CTkButton(self.btn_frame, text="Dodaj Pozycję", command=self.add_line_to_queue)
        self.btn_add_line.pack(side="right", padx=5)

        self.btn_clone_line = ctk.CTkButton(self.btn_frame, text="Klonuj Pozycję", fg_color="blue", command=lambda: self.add_line_to_queue(clone=True))
        self.btn_clone_line.pack(side="right", padx=5)

        # Lines Queue Table (Treeview)
        self.queue_frame = ctk.CTkFrame(self.form_frame, height=150)
        self.queue_frame.grid(row=12, column=0, columnspan=2, pady=10, sticky="nsew")
        self.queue_frame.pack_propagate(False)
        
        columns = ("wn", "ma", "amount", "wn_id", "ma_id")
        self.tree = ttk.Treeview(self.queue_frame, columns=columns, show="headings", height=5)
        self.tree.heading("wn", text="Konto WN")
        self.tree.heading("ma", text="Konto MA")
        self.tree.heading("amount", text="Kwota")
        self.tree.column("wn", width=150)
        self.tree.column("ma", width=150)
        self.tree.column("amount", width=100, anchor="e")
        self.tree.column("wn_id", width=0, stretch=tk.NO)
        self.tree.column("ma_id", width=0, stretch=tk.NO)
        self.tree.pack(fill="both", expand=True)
        
        # Final Save Button and Status
        self.btn_save = ctk.CTkButton(self.form_frame, text="Zapisz Dokument", fg_color="green", command=self.save_document)
        self.btn_save.grid(row=13, column=1, padx=5, pady=(10, 20), sticky="e")
        
        self.lbl_status = ctk.CTkLabel(self.form_frame, text="")
        self.lbl_status.grid(row=13, column=0, padx=5, pady=(10, 20), sticky="w")


        # ==== AI Suggestions Frame ====
        self.ai_frame = ctk.CTkFrame(self)
        self.ai_frame.grid(row=1, column=1, sticky="nsew", padx=(10,20), pady=(0, 20))
        
        self.ai_lbl = ctk.CTkLabel(self.ai_frame, text="✨ Sugestie AI", font=ctk.CTkFont(weight="bold", size=16))
        self.ai_lbl.pack(pady=15)
        
        self.ai_content = ctk.CTkFrame(self.ai_frame, fg_color="transparent")
        self.ai_content.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.show_ai_placeholder()

    def load_recent_accounts(self):
        # Clear existing buttons
        for widget in self.recent_wn_frame.winfo_children():
            widget.destroy()
        for widget in self.recent_ma_frame.winfo_children():
            widget.destroy()
            
        recent_wn_ids = []
        recent_ma_ids = []
        
        # Get latest distinct WN
        lines_wn = DocumentLine.select(DocumentLine.account_wn_id).group_by(DocumentLine.account_wn_id).order_by(DocumentLine.id.desc()).limit(5)
        recent_wn_ids = [line.account_wn_id for line in lines_wn if line.account_wn_id]
        
        # Get latest distinct MA
        lines_ma = DocumentLine.select(DocumentLine.account_ma_id).group_by(DocumentLine.account_ma_id).order_by(DocumentLine.id.desc()).limit(5)
        recent_ma_ids = [line.account_ma_id for line in lines_ma if line.account_ma_id]
        
        def create_recent_btns(parent, account_ids, acc_type):
            for acc_id in account_ids:
                acc = Account.get_or_none(Account.id == acc_id)
                if acc:
                    btn = ctk.CTkButton(parent, text=acc.symbol, width=40, font=ctk.CTkFont(size=10), 
                                        command=lambda a_id=acc.id, a_sym=acc.symbol, a_name=acc.name: self.apply_quick_account(acc_type, a_id, a_sym, a_name))
                    btn.pack(side="left", padx=2)

        create_recent_btns(self.recent_wn_frame, recent_wn_ids, "wn")
        create_recent_btns(self.recent_ma_frame, recent_ma_ids, "ma")

    def apply_quick_account(self, acc_type, acc_id, symbol, name):
        if acc_type == "wn":
            self.account_wn_id = acc_id
            self.btn_wn.configure(text=f"{symbol} - {name}")
        else:
            self.account_ma_id = acc_id
            self.btn_ma.configure(text=f"{symbol} - {name}")

    def show_ai_placeholder(self, text="Wprowadź opis i odznacz pole,\naby otrzymać sugestie dektretacji."):
        for widget in self.ai_content.winfo_children():
            widget.destroy()
        lbl = ctk.CTkLabel(self.ai_content, text=text, text_color="gray")
        lbl.pack(pady=20)

    def open_contractor_modal(self):
        def fetch_contractors(phrase):
            all_contractors = Contractor.select().order_by(Contractor.name)
            if not phrase:
                return [(c.id, c.nip or "-", c.name) for c in all_contractors]
                
            clean_phrase = phrase.replace("-", "").replace(" ", "").lower()
            results = []
            for c in all_contractors:
                c_nip = (c.nip or "").replace("-", "").replace(" ", "").lower()
                c_name = c.name.lower()
                if clean_phrase in c_nip or clean_phrase in c_name:
                    results.append((c.id, c.nip or "-", c.name))
            return results
            
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
            all_accounts = Account.select().order_by(Account.symbol)
            if not phrase:
                return [(a.id, a.symbol, a.name) for a in all_accounts]
                
            clean_phrase = phrase.replace("-", "").replace(" ", "").lower()
            results = []
            for a in all_accounts:
                a_symbol = a.symbol.replace("-", "").replace(" ", "").lower()
                a_name = a.name.lower()
                if clean_phrase in a_symbol or clean_phrase in a_name:
                    results.append((a.id, a.symbol, a.name))
            return results
            
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

    def add_line_to_queue(self, clone=False):
        wn_id = self.account_wn_id
        ma_id = self.account_ma_id
        amount = self.entry_amount.get().strip()

        if not all([wn_id, ma_id, amount]):
            self.lbl_status.configure(text="Błąd: Uzupełnij kwotę i oba konta przed dodaniem pozycji.", text_color="red")
            return
            
        wn_display = self.btn_wn.cget("text")
        ma_display = self.btn_ma.cget("text")
        
        try:
            float_amount = float(amount.replace(',', '.'))
        except ValueError:
            self.lbl_status.configure(text="Błąd: Błędny format kwoty.", text_color="red")
            return

        self.tree.insert("", "end", values=(wn_display, ma_display, f"{float_amount:.2f}", wn_id, ma_id))
        self.lbl_status.configure(text=f"Dodano pozycję. W kolejce: {len(self.tree.get_children())}", text_color="green")
        
        # Clear fields only if not cloning
        if not clone:
            self.entry_amount.delete(0, 'end')
            self.btn_wn.configure(text="Wybierz Konto WN")
            self.account_wn_id = None
            self.btn_ma.configure(text="Wybierz Konto MA")
            self.account_ma_id = None

    def save_document(self):
        doc_type = self.combo_type.get()
        number = self.entry_number.get()
        date_issue = self.entry_date.get()
        desc = self.txt_desc.get("1.0", "end-1c").strip()
        contractor_id = self.contractor_id
        queued_lines = self.tree.get_children()
        
        if not all([doc_type, number, date_issue, desc, contractor_id]):
            self.lbl_status.configure(text="Błąd: Wypełnij wszystkie pola w nagłówku!", text_color="red")
            return
            
        if not queued_lines:
            self.lbl_status.configure(text="Błąd: Brak pozycji dekretacyjnych do zapisu!", text_color="red")
            return

        try:
            # Calculate total header amount (sum of all queue lines)
            total_amount = sum(float(self.tree.item(item, 'values')[2]) for item in queued_lines)
            
            # Tworzymy dokument
            document = Document.create(
                document_type=doc_type,
                number=number,
                date_issue=date_issue,
                description=desc,
                amount=total_amount,
                contractor_id=contractor_id
            )
            
            # Tworzymy linie dekretacyjne
            for item in queued_lines:
                values = self.tree.item(item, 'values')
                DocumentLine.create(
                    document=document,
                    account_wn_id=int(values[3]),
                    account_ma_id=int(values[4]),
                    amount=float(values[2])
                )
                
            self.lbl_status.configure(text=f"Zapisano Pomyślnie. {doc_type}: {number}. Suma: {total_amount:.2f}", text_color="green")
            
            # Doucz model "na żywo"
            if self.ai_engine:
                threading.Thread(target=self.ai_engine.train, daemon=True).start()
                
            # Wyczyść powłokę formularza i kolejkę by dodawać następny dokument
            self.entry_number.delete(0, 'end')
            self.txt_desc.delete("1.0", "end")
            self.btn_contractor.configure(text="Wybierz Kontrahenta")
            self.contractor_id = None
            self.entry_amount.delete(0, 'end')
            self.btn_wn.configure(text="Wybierz Konto WN")
            self.account_wn_id = None
            self.btn_ma.configure(text="Wybierz Konto MA")
            self.account_ma_id = None
            self.show_ai_placeholder()
            self.load_recent_accounts()
            for row in queued_lines:
                self.tree.delete(row)
            
        except Exception as e:
            self.lbl_status.configure(text=f"Błąd zapisu: {e}", text_color="red")
