import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from datetime import date
from kontakt.database.models import Contractor, SalesInvoice, SalesInvoiceItem, ProductCatalog
from kontakt.ui.components.selection_modal import SelectionModal

class InvoiceCreatorView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        
        # Main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.header = ctk.CTkLabel(self, text="Wystaw Fakturę Sprzedaży", font=ctk.CTkFont(size=24, weight="bold"))
        self.header.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Content Scrollable Frame
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        
        # ==== 1. Invoice Header Data ====
        self.frame_head = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.frame_head.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.frame_head.grid_columnconfigure((0, 1), weight=1)

        # Lewa kolumna nagłówka (Daty i numer)
        self.lbl_number = ctk.CTkLabel(self.frame_head, text="Numer Faktury:")
        self.lbl_number.grid(row=0, column=0, padx=5, pady=(5, 0), sticky="w")
        self.entry_number = ctk.CTkEntry(self.frame_head, placeholder_text="FV/2026/01/01")
        self.entry_number.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="ew")

        self.lbl_date_issue = ctk.CTkLabel(self.frame_head, text="Data Wystawienia:")
        self.lbl_date_issue.grid(row=2, column=0, padx=5, pady=(5, 0), sticky="w")
        self.entry_date_issue = ctk.CTkEntry(self.frame_head)
        self.entry_date_issue.insert(0, str(date.today()))
        self.entry_date_issue.grid(row=3, column=0, padx=5, pady=(0, 10), sticky="ew")
        
        self.lbl_date_sale = ctk.CTkLabel(self.frame_head, text="Data Sprzedaży:")
        self.lbl_date_sale.grid(row=4, column=0, padx=5, pady=(5, 0), sticky="w")
        self.entry_date_sale = ctk.CTkEntry(self.frame_head)
        self.entry_date_sale.insert(0, str(date.today()))
        self.entry_date_sale.grid(row=5, column=0, padx=5, pady=(0, 10), sticky="ew")

        # Prawa kolumna nagłówka (Kontrahent i płatność)
        self.contractor_id = None
        self.lbl_contractor = ctk.CTkLabel(self.frame_head, text="Nabywca:")
        self.lbl_contractor.grid(row=0, column=1, padx=5, pady=(5, 0), sticky="w")
        
        self.btn_contractor = ctk.CTkButton(self.frame_head, text="Wybierz Nabywcę", fg_color="transparent", border_width=1, text_color=("gray10", "gray90"), anchor="w", command=self.open_contractor_modal)
        self.btn_contractor.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="ew")

        self.lbl_payment = ctk.CTkLabel(self.frame_head, text="Metoda Płatności:")
        self.lbl_payment.grid(row=2, column=1, padx=5, pady=(5, 0), sticky="w")
        self.combo_payment = ctk.CTkComboBox(self.frame_head, values=["przelew", "gotówka", "karta"])
        self.combo_payment.grid(row=3, column=1, padx=5, pady=(0, 10), sticky="ew")

        self.lbl_due_date = ctk.CTkLabel(self.frame_head, text="Termin Płatności:")
        self.lbl_due_date.grid(row=4, column=1, padx=5, pady=(5, 0), sticky="w")
        self.entry_due_date = ctk.CTkEntry(self.frame_head)
        self.entry_due_date.insert(0, str(date.today()))
        self.entry_due_date.grid(row=5, column=1, padx=5, pady=(0, 10), sticky="ew")

        # ==== 2. Items Adding Form ====
        self.lbl_items_title = ctk.CTkLabel(self.scroll_frame, text="2. Pozycje na fakturze", font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_items_title.grid(row=1, column=0, sticky="w", pady=(10, 5))
        
        self.frame_item = ctk.CTkFrame(self.scroll_frame)
        self.frame_item.grid(row=2, column=0, sticky="ew", pady=(0, 10), ipadx=10, ipady=10)
        
        # Wyszukiwarka z katalogu
        self.btn_catalog = ctk.CTkButton(self.frame_item, text="Wybierz z Katalogu", command=self.open_catalog_modal)
        self.btn_catalog.grid(row=0, column=0, columnspan=2, padx=5, pady=(10, 15), sticky="w")
        
        # Pola pozycji
        self.lbl_item_name = ctk.CTkLabel(self.frame_item, text="Nazwa Usługi/Produktu:")
        self.lbl_item_name.grid(row=1, column=0, padx=5, sticky="w")
        self.entry_item_name = ctk.CTkEntry(self.frame_item, width=250)
        self.entry_item_name.grid(row=2, column=0, padx=5, pady=(0, 10), sticky="w")

        self.lbl_item_qty = ctk.CTkLabel(self.frame_item, text="Ilość:")
        self.lbl_item_qty.grid(row=1, column=1, padx=5, sticky="w")
        self.entry_item_qty = ctk.CTkEntry(self.frame_item, width=80)
        self.entry_item_qty.insert(0, "1")
        self.entry_item_qty.grid(row=2, column=1, padx=5, pady=(0, 10), sticky="w")

        self.lbl_item_price = ctk.CTkLabel(self.frame_item, text="Cena Netto:")
        self.lbl_item_price.grid(row=1, column=2, padx=5, sticky="w")
        self.entry_item_price = ctk.CTkEntry(self.frame_item, width=100)
        self.entry_item_price.grid(row=2, column=2, padx=5, pady=(0, 10), sticky="w")

        self.lbl_item_vat = ctk.CTkLabel(self.frame_item, text="VAT (%):")
        self.lbl_item_vat.grid(row=1, column=3, padx=5, sticky="w")
        self.combo_item_vat = ctk.CTkComboBox(self.frame_item, values=["23", "8", "5", "0", "zw"], width=80)
        self.combo_item_vat.grid(row=2, column=3, padx=5, pady=(0, 10), sticky="w")

        self.btn_add_item = ctk.CTkButton(self.frame_item, text="Dodaj do Listy", command=self.add_item_to_queue)
        self.btn_add_item.grid(row=2, column=4, padx=15, pady=(0, 10), sticky="w")

        # ==== 3. Items Queue Table ====
        self.queue_frame = ctk.CTkFrame(self.scroll_frame, height=200)
        self.queue_frame.grid(row=3, column=0, sticky="nsew", pady=10)
        self.queue_frame.pack_propagate(False)
        
        columns = ("name", "qty", "price_net", "vat_rate", "total_net", "total_gross")
        self.tree = ttk.Treeview(self.queue_frame, columns=columns, show="headings", height=8)
        self.tree.heading("name", text="Nazwa")
        self.tree.heading("qty", text="Ilość")
        self.tree.heading("price_net", text="Cena Netto")
        self.tree.heading("vat_rate", text="VAT")
        self.tree.heading("total_net", text="Wartość Netto")
        self.tree.heading("total_gross", text="Wartość Brutto")
        
        self.tree.column("name", width=250)
        self.tree.column("qty", width=60, anchor="center")
        self.tree.column("price_net", width=100, anchor="e")
        self.tree.column("vat_rate", width=60, anchor="center")
        self.tree.column("total_net", width=100, anchor="e")
        self.tree.column("total_gross", width=100, anchor="e")
        self.tree.pack(fill="both", expand=True)

        # Totals Display
        self.lbl_totals = ctk.CTkLabel(self.scroll_frame, text="Suma Netto: 0.00 PLN  |  Suma VAT: 0.00 PLN  |  Suma Brutto: 0.00 PLN", font=ctk.CTkFont(weight="bold"))
        self.lbl_totals.grid(row=4, column=0, sticky="e", pady=10)

        # Action Buttons
        self.bottom_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.bottom_frame.grid(row=5, column=0, sticky="ew", pady=20)
        
        self.lbl_status = ctk.CTkLabel(self.bottom_frame, text="")
        self.lbl_status.pack(side="left", padx=5)
        
        self.btn_save = ctk.CTkButton(self.bottom_frame, text="Wystaw Fakturę", fg_color="green", command=self.save_invoice)
        self.btn_save.pack(side="right", padx=5)
        
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
            self.master,
            title="Wybierz Nabywcę",
            columns=[("id", "ID", 0), ("nip", "NIP", 100), ("name", "Nazwa", 400)],
            data_fetcher=fetch_contractors,
            on_select=on_select
        )

    def open_catalog_modal(self):
        def fetch_products(phrase):
            all_products = ProductCatalog.select().order_by(ProductCatalog.name)
            if phrase:
                phrase = phrase.lower()
                all_products = [p for p in all_products if phrase in p.name.lower()]
            return [(p.id, p.name, f"{p.price_net:.2f}", p.vat_rate) for p in all_products]

        def on_select(values):
            # values = (id, name, price_net, vat_rate)
            self.entry_item_name.delete(0, 'end')
            self.entry_item_name.insert(0, values[1])
            
            self.entry_item_price.delete(0, 'end')
            self.entry_item_price.insert(0, values[2])
            
            self.combo_item_vat.set(values[3])
            
        SelectionModal(
            self.master,
            title="Wybierz Produkt/Usługę",
            columns=[("id", "ID", 0), ("name", "Nazwa", 250), ("price", "Cena Netto", 80), ("vat", "VAT", 50)],
            data_fetcher=fetch_products,
            on_select=on_select
        )

    def add_item_to_queue(self):
        name = self.entry_item_name.get().strip()
        qty_str = self.entry_item_qty.get().strip()
        price_str = self.entry_item_price.get().strip()
        vat_str = self.combo_item_vat.get()
        
        if not name or not qty_str or not price_str:
            self.lbl_status.configure(text="Błąd: Uzupełnij nazwę, ilość i cenę.", text_color="red")
            return
            
        try:
            qty = float(qty_str.replace(',', '.'))
            price_net = float(price_str.replace(',', '.'))
            
            total_net = qty * price_net
            
            if vat_str.isdigit():
                vat_amount = total_net * (float(vat_str) / 100.0)
            else:
                vat_amount = 0.0 # 'zw' etc
                
            total_gross = total_net + vat_amount
            
            self.tree.insert("", "end", values=(
                name,
                f"{qty:.2f}",
                f"{price_net:.2f}",
                vat_str,
                f"{total_net:.2f}",
                f"{total_gross:.2f}"
            ))
            
            self.lbl_status.configure(text="", text_color="green")
            self.update_totals()
            
            # Clear row
            self.entry_item_name.delete(0, 'end')
            self.entry_item_qty.delete(0, 'end')
            self.entry_item_qty.insert(0, "1")
            self.entry_item_price.delete(0, 'end')
            
        except ValueError:
            self.lbl_status.configure(text="Błąd: Nieprawidłowy format kwoty lub ilości.", text_color="red")
            
    def update_totals(self):
        sum_net = 0.0
        sum_gross = 0.0
        
        for item in self.tree.get_children():
            vals = self.tree.item(item, 'values')
            sum_net += float(vals[4])
            sum_gross += float(vals[5])
            
        sum_vat = sum_gross - sum_net
        self.lbl_totals.configure(text=f"Suma Netto: {sum_net:.2f} PLN  |  Suma VAT: {sum_vat:.2f} PLN  |  Suma Brutto: {sum_gross:.2f} PLN")

    def save_invoice(self):
        number = self.entry_number.get().strip()
        date_issue = self.entry_date_issue.get()
        date_sale = self.entry_date_sale.get()
        due_date = self.entry_due_date.get()
        payment = self.combo_payment.get()
        contractor_id = self.contractor_id
        queued_lines = self.tree.get_children()
        
        if not all([number, date_issue, date_sale, due_date]):
            self.lbl_status.configure(text="Błąd: Wypełnij wszystkie daty i numer!", text_color="red")
            return
            
        if not contractor_id:
            self.lbl_status.configure(text="Błąd: Wybierz Nabywcę!", text_color="red")
            return
            
        if not queued_lines:
            self.lbl_status.configure(text="Błąd: Faktura musi mieć co najmniej jedną pozycję.", text_color="red")
            return
            
        try:
            # Tworzymy fakturę główną
            invoice = SalesInvoice.create(
                number=number,
                date_issue=date_issue,
                date_sale=date_sale,
                due_date=due_date,
                contractor_id=contractor_id,
                payment_method=payment
            )
            
            for item in queued_lines:
                vals = self.tree.item(item, 'values')
                SalesInvoiceItem.create(
                    invoice=invoice,
                    product_name=vals[0],
                    quantity=float(vals[1]),
                    price_net=float(vals[2]),
                    vat_rate=vals[3],
                    total_net=float(vals[4]),
                    total_gross=float(vals[5])
                )
                
            self.lbl_status.configure(text=f"Sukces! Wystawiono Fakturę {number}", text_color="green")
            
            # Reset
            self.entry_number.delete(0, 'end')
            self.contractor_id = None
            self.btn_contractor.configure(text="Wybierz Nabywcę")
            for item in queued_lines:
                self.tree.delete(item)
            self.update_totals()
            
        except Exception as e:
            self.lbl_status.configure(text=f"Błąd zapisu: {e}", text_color="red")
