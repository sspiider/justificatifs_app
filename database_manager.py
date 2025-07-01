import sqlite3
import pandas as pd

class DatabaseManager:
    def __init__(self, db_path="database/justificatifs.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        """Crée la table si elle n'existe pas"""
        query = """
        CREATE TABLE IF NOT EXISTS justificatifs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            montant REAL,
            tva TEXT,
            fichier_original TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def save_data(self, date, montant, tva, filename):
        """Enregistre les données extraites"""
        query = """
        INSERT INTO justificatifs (date, montant, tva, fichier_original)
        VALUES (?, ?, ?, ?)
        """
        self.conn.execute(query, (date, montant, tva, filename))
        self.conn.commit()

    def export_to_csv(self, csv_path="export.csv"):
        """Exporte les données en CSV"""
        df = pd.read_sql("SELECT * FROM justificatifs", self.conn)
        df.to_csv(csv_path, index=False)
        return csv_path
