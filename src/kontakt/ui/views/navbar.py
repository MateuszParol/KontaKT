import customtkinter as ctk

class Navbar(ctk.CTkFrame):
    def __init__(self, master, navigate_callback):
        super().__init__(master, height=60, corner_radius=0)
        self.navigate_callback = navigate_callback
        
        # Logo on the left
        self.logo_label = ctk.CTkLabel(self, text="KontaKT", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(side="left", padx=(20, 30), pady=10)
        
        # Navigation Buttons
        self.btn_new = self.create_button("Dokumenty", "invoice_add")
        self.btn_history = self.create_button("Historia", "history")
        self.btn_accounts = self.create_button("Plan Kont", "accounts")
        self.btn_contractors = self.create_button("Kontrahenci", "contractors")
        
        # Spacer
        spacer = ctk.CTkFrame(self, fg_color="transparent", height=0)
        spacer.pack(side="left", fill="x", expand=True)

        # Settings on the right
        self.btn_settings = self.create_button("Ustawienia", "settings", right=True)

    def create_button(self, text, view_name, right=False):
        btn = ctk.CTkButton(self, text=text, fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), command=lambda: self.navigate_callback(view_name))
        if right:
            btn.pack(side="right", padx=10, pady=10)
        else:
            btn.pack(side="left", padx=5, pady=10)
        return btn
