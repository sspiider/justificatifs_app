from pdf2image import convert_from_path
import os

class PDFProcessor:
    @staticmethod
    def extract_text_from_pdf(pdf_path):
        """Extrait le texte des PDF natifs (non scannés)"""
        with open(pdf_path, 'rb') as file:
            pdf = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
            return text

    @staticmethod
    def convert_pdf_to_img(pdf_path, output_folder="temp_files"):
        """Convertit les PDF scannés en images pour l'OCR"""
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        images = convert_from_path(pdf_path, output_folder=output_folder)
        return images[0].filename  # Retourne le chemin de la 1ère image
