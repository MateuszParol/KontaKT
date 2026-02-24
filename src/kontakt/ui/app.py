
import customtkinter as ctk
from kontakt import config
from kontakt.ui.views.navbar import Navbar
from kontakt.ui.views.document_add import DocumentAddView
from kontakt.ui.views.accounts import AccountsView
from kontakt.ui.views.contractors import ContractorsView
import threading
from tkinter import ttk
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

        # Configure scaling and ttk styles for Treeview
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2b2b2b",
                        foreground="white",
                        rowheight=35,
                        fieldbackground="#2b2b2b",
                        bordercolor="#2b2b2b",
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#1f538d')])
        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="flat",
                        padding=5)
        style.map("Treeview.Heading",
                  background=[('active', '#343638')])
        
        # Configure Vertical Scrollbar style
        style.configure("Vertical.TScrollbar", background="#2b2b2b", bordercolor="#2b2b2b", arrowcolor="white", troughcolor="#2b2b2b")


        # Layout configuration (2x1)
        self.grid_columnconfigure(0, weight=1) # Content flexible
        self.grid_rowconfigure(0, weight=0) # Navbar fixed
        self.grid_rowconfigure(1, weight=1) # Content flexible

        # Navbar
        self.navbar = Navbar(self, self.show_view)
        self.navbar.grid(row=0, column=0, sticky="ew")

        # Content Area (Frame)
        self.content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew")

        # Init default view
        self.show_view("document_add")

    def show_view(self, view_name):
        # Hide/Destroy current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Show new view
        if view_name == "document_add":
            view = DocumentAddView(self.content_frame, ai_engine=self.ai_engine)
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
