import customtkinter as ctk
from tkinter import ttk

class SelectionModal(ctk.CTkToplevel):
    def __init__(self, master, title, columns, data_fetcher, on_select):
        """
        :param data_fetcher: Function taking a search string and returning a list of dicts/tuples
        :param on_select: Callback function taking the selected item values
        """
        super().__init__(master)
        
        self.title(title)
        self.geometry("600x400")
        self.resizable(False, False)
        
        self.data_fetcher = data_fetcher
        self.on_select_callback = on_select
        
        # UI Setup
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Search Frame
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.entry_search = ctk.CTkEntry(self.search_frame, placeholder_text="Wpisz by wyszukać...")
        self.entry_search.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_search.bind("<KeyRelease>", self.on_search)
        
        # Treeview Frame
        self.tree_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.tree_frame.grid(row=1, column=0, padx=10, sticky="nsew")
        self.tree_frame.grid_columnconfigure(0, weight=1)
        self.tree_frame.grid_rowconfigure(0, weight=1)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=[c[0] for c in columns], show="headings", selectmode="browse")
        for col_id, col_text, col_width in columns:
            self.tree.heading(col_id, text=col_text, anchor="w")
            self.tree.column(col_id, width=col_width, stretch=True)
            
        self.tree.bind("<Double-1>", lambda e: self.confirm_selection())
        
        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview, style="Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Bottom Buttons
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        self.btn_cancel = ctk.CTkButton(self.btn_frame, text="Anuluj", fg_color="gray", command=self.destroy)
        self.btn_cancel.pack(side="right", padx=(5, 0))
        
        self.btn_select = ctk.CTkButton(self.btn_frame, text="Wybierz", command=self.confirm_selection)
        self.btn_select.pack(side="right")
        
        self.refresh_list()
        
        # Make modal blocking
        self.transient(master)
        self.grab_set()
        self.wait_window()
        
    def on_search(self, event):
        self.refresh_list()
        
    def refresh_list(self):
        self.tree.delete(*self.tree.get_children())
        phrase = self.entry_search.get().strip()
        
        results = self.data_fetcher(phrase)
        for idx, item in enumerate(results):
            # item should be an iterable matching columns order
            self.tree.insert("", "end", iid=str(idx), values=item)
            # Store full original item if needed, but we pass values string representations
            
    def confirm_selection(self):
        selected = self.tree.selection()
        if not selected:
            return
            
        item = self.tree.item(selected[0])
        values = item['values']
        self.on_select_callback(values)
        self.destroy()
