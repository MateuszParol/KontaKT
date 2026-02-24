import customtkinter as ctk
from kontakt.database.models import Settings

class SettingsView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.header = ctk.CTkLabel(self, text="Ustawienia Aplikacji", font=ctk.CTkFont(size=24, weight="bold"))
        self.header.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Content Scrollable Frame
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        
        # ==== Section 1: KSeF Seller Data ====
        self.frame_ksef = ctk.CTkFrame(self.scroll_frame)
        self.frame_ksef.grid(row=0, column=0, sticky="ew", pady=(0, 20), ipadx=20, ipady=20)
        self.frame_ksef.grid_columnconfigure(1, weight=1)
        
        lbl_ksef_title = ctk.CTkLabel(self.frame_ksef, text="Dane Podmiotu (Sprzedawca KSeF)", font=ctk.CTkFont(size=16, weight="bold"))
        lbl_ksef_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

        # NIP
        ctk.CTkLabel(self.frame_ksef, text="NIP (bez myślników):").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_nip = ctk.CTkEntry(self.frame_ksef)
        self.entry_nip.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        # Nazwa
        ctk.CTkLabel(self.frame_ksef, text="Pełna Nazwa Urzędu:").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_name = ctk.CTkEntry(self.frame_ksef)
        self.entry_name.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        
        # Addres
        ctk.CTkLabel(self.frame_ksef, text="Kod Pocztowy:").grid(row=3, column=0, sticky="w", pady=5)
        self.entry_zip = ctk.CTkEntry(self.frame_ksef)
        self.entry_zip.grid(row=3, column=1, sticky="w", padx=10, pady=5)
        
        ctk.CTkLabel(self.frame_ksef, text="Miejscowość:").grid(row=4, column=0, sticky="w", pady=5)
        self.entry_city = ctk.CTkEntry(self.frame_ksef)
        self.entry_city.grid(row=4, column=1, sticky="ew", padx=10, pady=5)
        
        ctk.CTkLabel(self.frame_ksef, text="Ulica i numer:").grid(row=5, column=0, sticky="w", pady=5)
        self.entry_street = ctk.CTkEntry(self.frame_ksef)
        self.entry_street.grid(row=5, column=1, sticky="ew", padx=10, pady=5)

        # Zapisz
        self.btn_save = ctk.CTkButton(self.scroll_frame, text="Zapisz Ustawienia", command=self.save_settings, fg_color="green")
        self.btn_save.grid(row=1, column=0, sticky="e", pady=10)
        
        self.lbl_status = ctk.CTkLabel(self.scroll_frame, text="")
        self.lbl_status.grid(row=2, column=0, sticky="e")
        
        # Init
        self.load_settings()

    def load_settings(self):
        try:
            settings_dict = {s.key: s.value for s in Settings.select()}
            
            if "ksef_nip" in settings_dict:
                self.entry_nip.insert(0, settings_dict["ksef_nip"])
            if "ksef_name" in settings_dict:
                self.entry_name.insert(0, settings_dict["ksef_name"])
            if "ksef_zip" in settings_dict:
                self.entry_zip.insert(0, settings_dict["ksef_zip"])
            if "ksef_city" in settings_dict:
                self.entry_city.insert(0, settings_dict["ksef_city"])
            if "ksef_street" in settings_dict:
                self.entry_street.insert(0, settings_dict["ksef_street"])
        except Exception as e:
            self.lbl_status.configure(text=f"Błąd wczytywania ustawień: {e}", text_color="red")
            
    def save_settings(self):
        try:
            data = {
                "ksef_nip": self.entry_nip.get().strip(),
                "ksef_name": self.entry_name.get().strip(),
                "ksef_zip": self.entry_zip.get().strip(),
                "ksef_city": self.entry_city.get().strip(),
                "ksef_street": self.entry_street.get().strip()
            }
            
            for k, v in data.items():
                s, created = Settings.get_or_create(key=k)
                s.value = v
                s.save()
                
            self.lbl_status.configure(text="Ustawienia zapisane pomyślnie!", text_color="green")
        except Exception as e:
            self.lbl_status.configure(text=f"Błąd zapisu ustawień: {e}", text_color="red")
