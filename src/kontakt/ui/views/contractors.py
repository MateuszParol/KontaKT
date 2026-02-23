
import customtkinter as ctk
from customtkinter import filedialog
from kontakt.database.models import Contractor
from kontakt.services.importer import import_contractors_from_excel

class ContractorsView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header Frame
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        self.header = ctk.CTkLabel(self.header_frame, text="Kontrahenci", font=ctk.CTkFont(size=24, weight="bold"))
        self.header.pack(side="left")

        # Search Bar
        self.entry_search = ctk.CTkEntry(self.header_frame, placeholder_text="Szukaj (NIP / Nazwa)...", width=250)
        self.entry_search.pack(side="left", padx=20)
        self.entry_search.bind("<KeyRelease>", self.on_search)

        self.btn_import = ctk.CTkButton(self.header_frame, text="Importuj z Excela (.xls)", command=self.import_from_excel)
        self.btn_import.pack(side="right")
        
        self.lbl_import_status = ctk.CTkLabel(self.header_frame, text="")
        self.lbl_import_status.pack(side="right", padx=10)

        # List Area
        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        # Add New Form
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        
        self.entry_nip = ctk.CTkEntry(self.form_frame, placeholder_text="NIP")
        self.entry_nip.pack(side="left", padx=10, pady=10)
        
        self.entry_name = ctk.CTkEntry(self.form_frame, placeholder_text="Nazwa Firmy")
        self.entry_name.pack(side="left", padx=10, pady=10, fill="x", expand=True)
        
        self.btn_add = ctk.CTkButton(self.form_frame, text="Dodaj", command=self.add_contractor)
        self.btn_add.pack(side="right", padx=10, pady=10)

        self.refresh_list()

    def on_search(self, event):
        self.refresh_list()

    def refresh_list(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        phrase = self.entry_search.get().strip()
        
        query = Contractor.select()
        if phrase:
            query = query.where(Contractor.name.contains(phrase) | Contractor.nip.contains(phrase))

        contractors = query.order_by(Contractor.name).limit(100)
        for c in contractors:
            lbl = ctk.CTkLabel(self.scroll_frame, text=f"{c.name} (NIP: {c.nip or '-'})", anchor="w")
            lbl.pack(fill="x", padx=5, pady=2)

    def add_contractor(self):
        nip = self.entry_nip.get()
        name = self.entry_name.get()
        if name:
            try:
                Contractor.create(nip=nip or None, name=name)
                self.entry_nip.delete(0, "end")
                self.entry_name.delete(0, "end")
                self.refresh_list()
            except Exception as e:
                print(f"Error adding contractor: {e}")

    def import_from_excel(self):
        filepath = filedialog.askopenfilename(
            title="Wybierz plik z Bazą Kontrahentów",
            filetypes=[("Pliki Excel", "*.xls *.xlsx")]
        )
        if not filepath:
            return
            
        self.lbl_import_status.configure(text="Importowanie...", text_color="orange")
        self.update()
        
        added, message = import_contractors_from_excel(filepath)
        
        if "Błąd" in message:
            self.lbl_import_status.configure(text=message, text_color="red")
        else:
            self.lbl_import_status.configure(text=message, text_color="green")
            self.refresh_list()
