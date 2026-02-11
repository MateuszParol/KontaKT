import customtkinter as ctk
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import os
from tkinter import messagebox, filedialog

# --- KONFIGURACJA WYGLĄDU ---
ctk.set_appearance_mode("System")  # Tryb: System, Light, Dark
ctk.set_default_color_theme("blue")  # Motyw kolorystyczny

# --- PLIK BAZY DANYCH ---
DB_FILE = "baza_wiedzy_jst.csv"

class BudgetBrain:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 2))
        self.model = NearestNeighbors(n_neighbors=1, metric='cosine')
        self.data = self.load_data()
        self.is_trained = False
        if not self.data.empty:
            self.train()

    def load_data(self):
        """Ładuje bazę wiedzy lub tworzy nową, jeśli nie istnieje."""
        if os.path.exists(DB_FILE):
            try:
                return pd.read_csv(DB_FILE)
            except Exception:
                return self.create_empty_db()
        else:
            return self.create_empty_db()

    def create_empty_db(self):
        """Tworzy strukturę pod JST."""
        df = pd.DataFrame(columns=['opis', 'dzial', 'rozdzial', 'paragraf', 'konto_wn', 'konto_ma'])
        # Dodajmy jeden przykładowy rekord startowy, żeby model nie był pusty
        new_row = pd.DataFrame({
            'opis': ['startowy wpis zakup materiałów biurowych papier'],
            'dzial': ['750'],
            'rozdzial': ['75023'],
            'paragraf': ['4210'],
            'konto_wn': ['401'],
            'konto_ma': ['201']
        })
        df = pd.concat([df, new_row], ignore_index=True)
        return df

    def save_data(self):
        self.data.to_csv(DB_FILE, index=False)

    def train(self):
        """Trenuje model na aktualnych danych."""
        if len(self.data) < 1:
            return
        self.tfidf_matrix = self.vectorizer.fit_transform(self.data['opis'].astype(str))
        self.model.fit(self.tfidf_matrix)
        self.is_trained = True

    def predict(self, text):
        """Zwraca sugestię klasyfikacji."""
        if not self.is_trained:
            return None
        
        vec = self.vectorizer.transform([text])
        distances, indices = self.model.kneighbors(vec)
        
        match_idx = indices[0][0]
        similarity = 1 - distances[0][0] # Pewność (0-1)
        
        result = self.data.iloc[match_idx].to_dict()
        result['pewnosc'] = round(similarity * 100, 2)
        return result

    def learn_new(self, opis, dzial, rozdzial, paragraf, wn, ma):
        """Dodaje nową wiedzę i przelicza model."""
        new_row = pd.DataFrame({
            'opis': [opis],
            'dzial': [dzial],
            'rozdzial': [rozdzial],
            'paragraf': [paragraf],
            'konto_wn': [wn],
            'konto_ma': [ma]
        })
        self.data = pd.concat([self.data, new_row], ignore_index=True)
        self.save_data()
        self.train()

# --- INTERFEJS GRAFICZNY (GUI) ---

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.brain = BudgetBrain()

        # Konfiguracja okna
        self.title("Asystent Księgowego JST v1.0")
        self.geometry("900x650")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Lewy panel (Menu)
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="BudżetAI", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, text="Nowa Dekretacja", command=self.show_main_view)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        
        self.sidebar_button_2 = ctk.CTkButton(self.sidebar_frame, text="Eksportuj Bazę", command=self.export_db)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        # Prawy panel (Główny)
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # --- Elementy Formularza ---
        
        # 1. Wejście
        self.lbl_opis = ctk.CTkLabel(self.main_frame, text="Wprowadź opis faktury:", font=("Arial", 14))
        self.lbl_opis.pack(pady=(10, 5), anchor="w", padx=20)
        
        self.entry_opis = ctk.CTkEntry(self.main_frame, placeholder_text="np. Zakup tonerów do drukarki dział kadr", width=600)
        self.entry_opis.pack(pady=5, padx=20)
        self.entry_opis.bind("<Return>", lambda event: self.analyze_invoice()) # Enter uruchamia analizę

        self.btn_analiza = ctk.CTkButton(self.main_frame, text="ANALIZUJ (Enter)", command=self.analyze_invoice, fg_color="green")
        self.btn_analiza.pack(pady=10, padx=20)

        # 2. Wyniki / Pola edycji
        self.results_frame = ctk.CTkFrame(self.main_frame)
        self.results_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.create_input_field("Dział:", "entry_dzial")
        self.create_input_field("Rozdział:", "entry_rozdzial")
        self.create_input_field("Paragraf:", "entry_paragraf")
        self.create_input_field("Konto WN:", "entry_wn")
        self.create_input_field("Konto MA:", "entry_ma")

        # Etykieta pewności
        self.lbl_confidence = ctk.CTkLabel(self.main_frame, text="Gotowy do pracy", text_color="gray")
        self.lbl_confidence.pack(pady=5)

        # 3. Akcje
        self.btn_save = ctk.CTkButton(self.main_frame, text="ZATWIERDŹ I NAUCZ (Zapisz)", command=self.save_and_learn, height=40)
        self.btn_save.pack(pady=20, padx=20, fill="x")

    def create_input_field(self, label_text, attr_name):
        """Pomocnicza funkcja do tworzenia ładnych pól."""
        frame = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        frame.pack(fill="x", pady=5)
        lbl = ctk.CTkLabel(frame, text=label_text, width=100, anchor="w")
        lbl.pack(side="left", padx=10)
        entry = ctk.CTkEntry(frame, width=300)
        entry.pack(side="left", expand=True, fill="x", padx=10)
        setattr(self, attr_name, entry)

    def show_main_view(self):
        pass # Placeholder

    def analyze_invoice(self):
        opis = self.entry_opis.get()
        if not opis:
            return
        
        sugestia = self.brain.predict(opis)
        
        # Wyczyszczenie pól
        self.clear_fields()
        
        if sugestia:
            self.entry_dzial.insert(0, sugestia['dzial'])
            self.entry_rozdzial.insert(0, sugestia['rozdzial'])
            self.entry_paragraf.insert(0, sugestia['paragraf'])
            self.entry_wn.insert(0, sugestia['konto_wn'])
            self.entry_ma.insert(0, sugestia['konto_ma'])
            
            pewnosc = sugestia['pewnosc']
            kolor = "green" if pewnosc > 80 else "orange" if pewnosc > 50 else "red"
            self.lbl_confidence.configure(text=f"Pewność systemu: {pewnosc}% (Na podstawie historii)", text_color=kolor)
        else:
            self.lbl_confidence.configure(text="Brak danych w historii. Wypełnij ręcznie, a zapamiętam.", text_color="white")

    def clear_fields(self):
        self.entry_dzial.delete(0, "end")
        self.entry_rozdzial.delete(0, "end")
        self.entry_paragraf.delete(0, "end")
        self.entry_wn.delete(0, "end")
        self.entry_ma.delete(0, "end")

    def save_and_learn(self):
        opis = self.entry_opis.get()
        dzial = self.entry_dzial.get()
        rozdzial = self.entry_rozdzial.get()
        paragraf = self.entry_paragraf.get()
        wn = self.entry_wn.get()
        ma = self.entry_ma.get()

        if not opis or not dzial:
            messagebox.showerror("Błąd", "Opis i Dział są wymagane!")
            return

        # Zapis do mózgu
        self.brain.learn_new(opis, dzial, rozdzial, paragraf, wn, ma)
        
        # Reset
        self.entry_opis.delete(0, "end")
        self.clear_fields()
        self.lbl_confidence.configure(text="Zapisano! System jest teraz mądrzejszy.", text_color="green")
        
        # Opcjonalnie: Przesunięcie fokusa z powrotem na opis
        self.entry_opis.focus()

    def export_db(self):
        self.brain.save_data()
        messagebox.showinfo("Eksport", f"Baza danych znajduje się w pliku: {DB_FILE}\nMożesz go otworzyć w Excelu.")

if __name__ == "__main__":
    app = App()
    app.mainloop()