from datetime import date

# =====================================================================
# KELAS UTILITY: LOCALIZER (PENERAPAN OOP - ENCAPSULATION)
# Kelas ini bertindak sebagai cetak biru (blueprint) khusus untuk 
# menangani manajemen dwi-bahasa (Inggris/Indonesia) dan format data.
# Memisahkan logika ini ke dalam Class tersendiri adalah bukti penerapan 
# "Single Responsibility Principle" (kode yang bersih dan termodularisasi).
# =====================================================================
class Localizer:
    
    # --- 1. KONSTRUKTOR OBJEK (INISIALISASI ATRIBUT) ---
    # Method bawaan penanda OOP. Dijalankan otomatis saat objek diciptakan 
    # untuk menyimpan "state" atau memori awal (kamus bahasa & nama bulan)
    # ke dalam variabel yang menempel pada wujud objek tersebut (self).
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

        # Kamus bulan bahasa Indonesia untuk mendukung rendering tanggal premium
        self.id_months = [
            "", "Januari", "Februari", "Maret", "April", "Mei", "Juni", 
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        ]

    # --- 2. METHOD: PENARIKAN TEKS (BEHAVIOR) ---
    # Kemampuan objek untuk menyajikan teks yang tepat secara dinamis
    # berdasarkan bahasa yang sedang dipilih oleh user di halaman utama.
    def get_text(self, key: str, lang: str) -> str:
        if key not in self.translations:
            return f"[{key}]"
        return self.translations[key].get(lang, self.translations[key]["EN"])

    # --- 3. METHOD: PEMFORMATAN MATA UANG ---
    # Kemampuan objek untuk mengonversi angka mentah hasil prediksi mesin
    # menjadi string bernuansa Luxury Brand (contoh: IDR 1,250,000 / gram).
    def format_currency(self, amount: float) -> str:
        """
        Formats the numerical valuation into a premium IDR string.
        Example: IDR 1,250,000 / gram
        """
        return f"IDR {amount:,.0f} / gram"

    # --- 4. METHOD: PEMFORMATAN TANGGAL ---
    # Kemampuan objek untuk merakit ulang tampilan objek datetime Python
    # menjadi teks tanggal yang estetik menyesuaikan lokalisasi bahasa.
    def format_date(self, d: date, lang: str) -> str:
        """
        Formats the date elegantly based on the selected language.
        """
        if lang == "ID":
            return f"{d.day:02d} {self.id_months[d.month]} {d.year}"
        else:
            return d.strftime("%B %d, %Y")
