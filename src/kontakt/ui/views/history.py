import customtkinter as ctk
from customtkinter import filedialog
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
        
        self.btn_export_all = ctk.CTkButton(self.header_frame, text="Eksportuj Dziennik (Excel)", fg_color="green", command=self.export_all_excel)
        self.btn_export_all.pack(side="right", padx=10)
        
        self.lbl_status = ctk.CTkLabel(self.header_frame, text="")
        self.lbl_status.pack(side="right", padx=10)

        # Columns Header
        self.cols_frame = ctk.CTkFrame(self)
        self.cols_frame.grid(row=1, column=0, padx=20, pady=(0,5), sticky="ew")
        self.cols_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
        ctk.CTkLabel(self.cols_frame, text="Data", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkLabel(self.cols_frame, text="Dokument", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkLabel(self.cols_frame, text="Kontrahent", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, padx=5, pady=5)
        ctk.CTkLabel(self.cols_frame, text="Kwota", font=ctk.CTkFont(weight="bold")).grid(row=0, column=3, padx=5, pady=5)
        ctk.CTkLabel(self.cols_frame, text="Akcje", font=ctk.CTkFont(weight="bold")).grid(row=0, column=4, padx=5, pady=5)

        # Scrollable List
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        self.refresh_list()

    def refresh_list(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        invoices = Invoice.select().order_by(Invoice.date_issue.desc())
        
        for inv in invoices:
            row_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)
            row_frame.grid_columnconfigure((0,1,2,3), weight=1)
            
            ctk.CTkLabel(row_frame, text=str(inv.date_issue)).grid(row=0, column=0, padx=5, pady=5)
            ctk.CTkLabel(row_frame, text=inv.number).grid(row=0, column=1, padx=5, pady=5)
            ctk.CTkLabel(row_frame, text=inv.contractor.name).grid(row=0, column=2, padx=5, pady=5)
            ctk.CTkLabel(row_frame, text=str(inv.amount)).grid(row=0, column=3, padx=5, pady=5)
            
            # Print PDF btn
            btn = ctk.CTkButton(row_frame, text="Pobierz PK (PDF)", width=100,
                                command=lambda i_id=inv.id, i_num=inv.number: self.download_pk(i_id, i_num))
            btn.grid(row=0, column=4, padx=5, pady=5)

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
