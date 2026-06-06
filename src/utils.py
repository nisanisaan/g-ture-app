from datetime import date

class Localizer:
    def __init__(self):
        """
        Initializes the bilingual dictionary and date configurations for G-Ture.
        """
        self.translations = {
            "title": {
                "EN": "The Future of Gold",
                "ID": "Masa Depan Emas"
            },
            "subtitle": {
                "EN": "Precision Forecasting for the 2026-2027 Horizon",
                "ID": "Prakiraan Presisi untuk Periode 2026-2027"
            },
            "select_date": {
                "EN": "Select Horizon Date",
                "ID": "Pilih Tanggal Proyeksi"
            },
            "btn_predict": {
                "EN": "Reveal Projection",
                "ID": "Tampilkan Proyeksi"
            },
            "result_label": {
                "EN": "Projected Valuation",
                "ID": "Estimasi Valuasi"
            },
            "error_model": {
                "EN": "Model vault is currently closed. (gold_model.pkl missing)",
                "ID": "Kubah model sedang ditutup. (gold_model.pkl tidak ditemukan)"
            }
        }

        # Indonesian month dictionary for premium date formatting
        self.id_months = [
            "", "Januari", "Februari", "Maret", "April", "Mei", "Juni", 
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        ]

    def get_text(self, key: str, lang: str) -> str:
        if key not in self.translations:
            return f"[{key}]"
        return self.translations[key].get(lang, self.translations[key]["EN"])

    def format_currency(self, amount: float) -> str:
        """
        Formats the numerical valuation into a premium IDR string.
        Example: IDR 1,250,000 / gram
        """
        return f"IDR {amount:,.0f} / gram"

    def format_date(self, d: date, lang: str) -> str:
        """
        Formats the date elegantly based on the selected language.
        """
        if lang == "ID":
            return f"{d.day:02d} {self.id_months[d.month]} {d.year}"
        else:
            return d.strftime("%B %d, %Y")