
import customtkinter as ctk
from kontakt import config
from kontakt.ui.views.sidebar import Sidebar
from kontakt.ui.views.invoice_add import InvoiceAddView
from kontakt.ui.views.accounts import AccountsView
from kontakt.ui.views.contractors import ContractorsView
import threading
from kontakt.ai.engine import AIEngine

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.ai_engine = AIEngine()
        # Train engine in background so it doesn't block UI
        threading.Thread(target=self.ai_engine.train, daemon=True).start()


        self.title("KontaKT - System Księgowości Budżetowej")
        self.geometry("1100x700")
        
        # Set theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Layout configuration (1x2)
        self.grid_columnconfigure(0, weight=0) # Sidebar fixed
        self.grid_columnconfigure(1, weight=1) # Content flexible
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = Sidebar(self, self.show_view)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Content Area (Frame)
        self.content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew")

        # Init default view
        self.show_view("invoice_add")

    def show_view(self, view_name):
        # Hide/Destroy current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Show new view
        if view_name == "invoice_add":
            view = InvoiceAddView(self.content_frame, ai_engine=self.ai_engine)
            view.pack(fill="both", expand=True)
        elif view_name == "history":
            from kontakt.ui.views.history import HistoryView
            view = HistoryView(self.content_frame)
            view.pack(fill="both", expand=True)
        elif view_name == "accounts":
            view = AccountsView(self.content_frame)
            view.pack(fill="both", expand=True)
        elif view_name == "contractors":
            view = ContractorsView(self.content_frame)
            view.pack(fill="both", expand=True)
        else:
            # Placeholder
            lbl = ctk.CTkLabel(self.content_frame, text=f"Widok: {view_name} (W budowie)", font=("Roboto", 24))
            lbl.pack(pady=50)
