import streamlit as st
from ocr_processor import OCRProcessor
from pdf_processor import PDFProcessor
from database_manager import DatabaseManager
import os
import tempfile

# --- Injection de Bootstrap 5 ---
bootstrap_css = """
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
"""
st.markdown(bootstrap_css, unsafe_allow_html=True)

# --- Interface Bootstrap stylisée ---
st.markdown("""
<div class="container mt-5">
    <h1 class="text-center text-primary mb-4">📄 Extracteur de Justificatifs Fiscaux</h1>
    <div class="card shadow p-4">
        <div class="card-body">
""", unsafe_allow_html=True)

# Initialisation
ocr = OCRProcessor()
pdf = PDFProcessor()
db = DatabaseManager()

# Interface Streamlit
st.title("📄 Extracteur de Justificatifs Fiscaux")

# Upload de fichier
uploaded_file = st.file_uploader("Téléverser un fichier (image/PDF)", type=["jpg", "png", "pdf"], key="uploader")

# --- Fermeture des balises HTML ---
st.markdown("""
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

if uploaded_file:
    # Sauvegarde temporaire du fichier
    temp_dir = "temp_files"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    temp_path = os.path.join(temp_dir, uploaded_file.name)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    try:
        # Traitement PDF ou Image
        if uploaded_file.type == "application/pdf":
            st.warning("Traitement des PDF...")
            text = pdf.extract_text_from_pdf(temp_path)
            if not text:  # Si PDF scanné
                img_path = pdf.convert_pdf_to_img(temp_path)
                texts = ocr.extract_text(img_path)
            else:
                texts = text.split('\n')
        else:
            texts = ocr.extract_text(temp_path)

        # Extraction des données
        data = ocr.extract_data(texts)
        
        # Affichage
        st.image(temp_path if uploaded_file.type != "application/pdf" else img_path, width=300)
        st.subheader("📋 Données extraites :")
        st.json(data)

        # Sauvegarde en base
        db.save_data(data["date"], data["montant"], data["tva"], uploaded_file.name)
        st.success("✅ Données enregistrées !")

        # Bouton d'export CSV
        if st.button("Exporter en CSV"):
            csv_path = db.export_to_csv()
            with open(csv_path, "rb") as f:
                st.download_button(
                    label="Télécharger CSV",
                    data=f,
                    file_name="export_justificatifs.csv",
                    mime="text/csv"
                )

    finally:
        # Nettoyage
        if os.path.exists(temp_path):
            os.remove(temp_path)
