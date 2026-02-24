import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from kontakt.database.models import Document, DocumentLine

class AIEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.model = MultinomialNB()
        self.is_trained = False
        self.classes_mapping = []  # Lista krotek (wn_id, ma_id)

    def train(self):
        """Trenuje model z zapisanych historycznych faktur."""
        # Pobieramy linie faktur wraz z opisem z powiązanej faktury
        query = (DocumentLine
                 .select(DocumentLine.account_wn_id, DocumentLine.account_ma_id, Document.description)
                 .join(Document)
                 .where(
                     Document.description.is_null(False),
                     Document.description != ""
                 ))
        
        X_raw = []
        y_raw = []
        for line in query:
            desc = line.document.description.strip()
            label = f"{line.account_wn_id}_{line.account_ma_id}"
            X_raw.append(desc)
            y_raw.append(label)

        if not X_raw:
            self.is_trained = False
            return

        # Uczymy TF-IDF
        X_vec = self.vectorizer.fit_transform(X_raw)
        
        # Uczymy model
        self.model.fit(X_vec, y_raw)
        
        # Zapamiętujemy mapowanie klas (scikit-learn trzyma klasy w self.model.classes_)
        # Klasy to stringi w formacie 'wnId_maId'
        self.classes_mapping = [tuple(map(int, c.split('_'))) for c in self.model.classes_]
        
        self.is_trained = True

    def predict(self, description: str, top_n: int = 3):
        """Zwraca Top N sugestii (listę słowników) dla danego opisu."""
        if not self.is_trained:
            return []
        
        desc = description.strip()
        if not desc:
            return []

        X_vec = self.vectorizer.transform([desc])
        
        try:
            probs = self.model.predict_proba(X_vec)[0]
        except Exception:
            return []

        # Sortujemy indeksy klas według prawdopodobieństwa malejąco
        top_indices = np.argsort(probs)[::-1][:top_n]
        
        results = []
        for idx in top_indices:
            wn_id, ma_id = self.classes_mapping[idx]
            match_percent = round(float(probs[idx]) * 100, 2)
            results.append({
                "account_wn_id": wn_id,
                "account_ma_id": ma_id,
                "match_percent": match_percent
            })
            
        return results
