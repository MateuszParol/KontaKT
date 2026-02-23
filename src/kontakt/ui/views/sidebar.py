
import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, navigate_callback):
        super().__init__(master, width=200, corner_radius=0)
        self.navigate_callback = navigate_callback
        
        self.logo_label = ctk.CTkLabel(self, text="KontaKT", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)
        
        # Buttons
        self.btn_new = self.create_button("Nowa Faktura", "invoice_add", 1)
        self.btn_history = self.create_button("Historia", "history", 2)
        self.btn_contractors = self.create_button("Kontrahenci", "contractors", 3)
        self.btn_accounts = self.create_button("Plan Kont", "accounts", 4)
        self.btn_settings = self.create_button("Ustawienia", "settings", 5)

    def create_button(self, text, view_name, row):
        btn = ctk.CTkButton(self, text=text, command=lambda: self.navigate_callback(view_name))
        btn.grid(row=row, column=0, padx=20, pady=10)
        return btn
