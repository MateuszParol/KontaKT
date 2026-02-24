import customtkinter as ctk
from customtkinter import filedialog
from tkinter import ttk
import os
import platform
import subprocess
from kontakt.database.models import Invoice
from kontakt.services.exporter import export_invoice_to_pdf, export_journal_to_excel

class HistoryView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Header Frame
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        self.header = ctk.CTkLabel(self.header_frame, text="Historia Operacji", font=ctk.CTkFont(size=24, weight="bold"))
        self.header.pack(side="left")

        # Search Bar
        self.entry_search = ctk.CTkEntry(self.header_frame, placeholder_text="Szukaj faktury...", width=250)
        self.entry_search.pack(side="left", padx=20)
        self.entry_search.bind("<KeyRelease>", self.on_search)
        
        self.btn_export_all = ctk.CTkButton(self.header_frame, text="Eksportuj Dziennik (Excel)", fg_color="green", command=self.export_all_excel)
        self.btn_export_all.pack(side="right", padx=10)
        
        self.lbl_status = ctk.CTkLabel(self.header_frame, text="")
        self.lbl_status.pack(side="right", padx=10)

        self.lbl_status.pack(side="right", padx=10)

        # Main List Area
        self.list_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.list_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_rowconfigure(0, weight=1)
        
        columns = ("id", "date", "number", "contractor", "amount")
        self.tree = ttk.Treeview(self.list_frame, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("id", text="ID") # Hidden column for logic
        self.tree.column("id", width=0, stretch=False) # Hide ID column 
        
        self.tree.heading("date", text="Data", anchor="w")
        self.tree.heading("number", text="Dokument", anchor="w")
        self.tree.heading("contractor", text="Kontrahent", anchor="w")
        self.tree.heading("amount", text="Kwota", anchor="w")
        
        self.tree.column("date", width=100, stretch=False)
        self.tree.column("number", width=150, stretch=False)
        self.tree.column("contractor", width=300, stretch=True)
        self.tree.column("amount", width=100, stretch=False)
        
        self.scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.tree.yview, style="Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Bottom Actions Frame
        self.actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.actions_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        self.btn_download_pk = ctk.CTkButton(self.actions_frame, text="Pobierz PK (PDF) dla wybranej faktury", command=self.download_selected_pk)
        self.btn_download_pk.pack(side="left")

        self.refresh_list()

    def on_search(self, event):
        self.refresh_list()

    def refresh_list(self):
        self.tree.delete(*self.tree.get_children())
            
        phrase = self.entry_search.get().strip()
        
        query = Invoice.select()
        if phrase:
            query = query.where(Invoice.number.contains(phrase) | Invoice.description.contains(phrase))

        invoices = query.order_by(Invoice.date_issue.desc())
        
        for inv in invoices:
            self.tree.insert("", "end", values=(inv.id, str(inv.date_issue), inv.number, inv.contractor.name, str(inv.amount)))

    def download_selected_pk(self):
        selected = self.tree.selection()
        if not selected:
            self.lbl_status.configure(text="Najpierw wybierz fakturę z listy.", text_color="orange")
            return
            
        item = self.tree.item(selected[0])
        invoice_id = item['values'][0]
        number = item['values'][2]
        
        self.download_pk(invoice_id, str(number))

    def download_pk(self, invoice_id, number):
        safe_num = "".join([c for c in number if c.isalpha() or c.isdigit() or c in " _-"]).rstrip()
        suggested = f"PK_{safe_num}.pdf"
        
        filepath = filedialog.asksaveasfilename(
            title="Zapisz Polecenie Księgowania",
            initialfile=suggested,
            defaultextension=".pdf",
            filetypes=[("Pliki PDF", "*.pdf")]
        )
        if not filepath:
            return
            
        success, msg = export_invoice_to_pdf(invoice_id, filepath)
        
        if success:
            self.lbl_status.configure(text="Zapisano PDF", text_color="green")
            self.open_file(filepath)
        else:
            self.lbl_status.configure(text=msg[:40], text_color="red")

    def export_all_excel(self):
        filepath = filedialog.asksaveasfilename(
            title="Zapisz Dziennik Księgowań",
            initialfile="Dziennik_KontaKT.xlsx",
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")]
        )
        if not filepath:
            return
            
        success, msg = export_journal_to_excel(filepath)
        
        if success:
            self.lbl_status.configure(text="Zapisano Excel", text_color="green")
            self.open_file(filepath)
        else:
            self.lbl_status.configure(text=msg[:40], text_color="red")

    def open_file(self, filepath):
        try:
            if platform.system() == 'Windows':
                os.startfile(filepath)
            elif platform.system() == 'Darwin':
                subprocess.call(('open', filepath))
            else:
                subprocess.call(('xdg-open', filepath))
        except Exception:
            pass # Ignoruj jeśli system nie umie otworzyć automatycznie
