
import customtkinter as ctk
from kontakt.database.models import Contractor

class ContractorsView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        self.header = ctk.CTkLabel(self, text="Kontrahenci", font=ctk.CTkFont(size=24, weight="bold"))
        self.header.grid(row=0, column=0, padx=20, pady=20, sticky="w")

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

    def refresh_list(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        contractors = Contractor.select().order_by(Contractor.name)
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
