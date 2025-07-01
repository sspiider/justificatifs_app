import easyocr
import re
import cv2

class OCRProcessor:
    def __init__(self, lang='fr'):
        self.reader = easyocr.Reader([lang])

    def extract_text(self, image_path):
        """Extrait le texte d'une image avec EasyOCR"""
        results = self.reader.readtext(image_path)
        return [text for (_, text, _) in results]

    def extract_data(self, texts):
        """Extrait les infos clés (date, montant, TVA) avec des regex"""
        data = {"date": None, "montant": None, "tva": None}
        for text in texts:
            # Extraction date (format JJ/MM/AAAA)
            if not data["date"]:
                date_match = re.search(r'\d{2}/\d{2}/\d{4}', text)
                if date_match: data["date"] = date_match.group()
            
            # Extraction montant (ex: 1 200,50 DH)
            if not data["montant"]:
                montant_match = re.search(r'\d+[\s,]+\d+,\d+', text)
                if montant_match: data["montant"] = montant_match.group()
            
            # Extraction numéro TVA (ex: TVA123456789)
            if not data["tva"]:
                tva_match = re.search(r'(TVA|T.V.A)\s*\d+', text, re.IGNORECASE)
                if tva_match: data["tva"] = tva_match.group()
        return data
