class ThemeManager:
    _instance = None
    
    # Singleton pattern
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ThemeManager, cls).__new__(cls, *args, **kwargs)
            cls._instance._init_theme()
        return cls._instance
        
    def _init_theme(self):
        self.current_mode = "dark" # "light" or "dark"
        
        # TOKYO NIGHT (Dark) Palette
        self._dark_theme = {
            "bg_main": "#1a1b26",          # Najciemniejsze tło (np. główny content)
            "bg_secondary": "#24283b",     # Tło dla Navbar, paneli, ramek
            "bg_tertiary": "#414868",      # Subtelne tło (np. zaznaczenie)
            "text_main": "#c0caf5",        # Główny tekst
            "text_muted": "#565f89",       # Szary tekst (nieaktywne)
            "accent_blue": "#7aa2f7",      # Główny akcent (niebieski)
            "accent_magenta": "#bb9af7",   # Poboczny akcent (fiolet)
            "accent_green": "#9ece6a",     # Informacja ok/zapis (zielony)
            "accent_red": "#f7768e",       # Błąd/Ostrzeżenie (czerwony)
            "accent_orange": "#ff9e64"     # Ostrzeżenie miękkie (pomarańcz)
        }
        
        # LIGHT PASTEL Palette (Odwrotność)
        self._light_theme = {
            "bg_main": "#f8f8f2",          # Bardzo jasne tło
            "bg_secondary": "#e2e2e3",     # Tło Navbar, panele
            "bg_tertiary": "#ccc",         # Zaznaczenie
            "text_main": "#282a36",        # Ciemny tekst (jak w Draculi)
            "text_muted": "#6272a4",       # Przygaszony tekst
            "accent_blue": "#2196f3",      # Standard blue
            "accent_magenta": "#9c27b0",   # Standard purple
            "accent_green": "#4caf50",     # Standard green
            "accent_red": "#f44336",       # Standard red
            "accent_orange": "#ff9800"
        }
        
    def get_color(self, color_name):
        theme = self._dark_theme if self.current_mode == "dark" else self._light_theme
        if color_name in theme:
            return theme[color_name]
        return "#ffffff" # Fallback
        
    def toggle_mode(self):
        self.current_mode = "light" if self.current_mode == "dark" else "dark"
        return self.current_mode
