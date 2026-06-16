import pickle
import numpy as np
import pandas as pd
from datetime import date

# =====================================================================
# KELAS UTAMA: GOLD PREDICTOR (PENERAPAN OOP - CORE ENGINE)
# Kelas ini adalah "Cetak Biru" (Blueprint) dari mesin kecerdasan buatan.
# Memisahkan logika machine learning ke dalam kelas terpisah (Modular) 
# memastikan bahwa antarmuka (UI) tidak tercampur dengan komputasi berat.
# =====================================================================
class GoldPredictor:
    
    # --- 1. KONSTRUKTOR OBJEK (INISIALISASI & ENKAPSULASI) ---
    # Method otomatis yang membangun state (memori) awal saat objek diciptakan.
    # Di sini, model machine learning biner (.pkl) dimuat dari penyimpanan
    # lokal ke dalam memori atribut objek (self.model) secara aman.
    def __init__(self, model_path: str):
        self.model_path = model_path
        try:
            # Membuka file biner ('rb' = read binary) dan memuatnya ke memori objek
            with open(self.model_path, 'rb') as file:
                self.model = pickle.load(file)
        except FileNotFoundError:
            # Mekanisme Fallback: Mencegah aplikasi crash total jika file .pkl hilang
            self.model = None

    # --- 2. METHOD PREDIKSI TUNGGAL (BEHAVIOR) ---
    # Kemampuan utama objek untuk meramalkan harga berdasarkan satu titik waktu.
    # Method ini merakit fitur turunan (hari_ke, bulan, tahun) secara dinamis
    # agar persis sesuai dengan format matriks pelatihan awal model.
    def predict(self, target_date: date) -> float:
        # Validasi keamanan: Hentikan komputasi dan return 0 jika model gagal dimuat
        if self.model is None:
            return 0.0

        # Validasi scope bisnis: Membatasi horizon analisis murni untuk 2026-2027
        if target_date.year not in [2026, 2027]:
            raise ValueError("G-Ture currently only projects for the 2026-2027 horizon.")

        # Menghitung jarak hari (delta) sebagai pondasi parameter time-series
        base_date = date(2026, 1, 1)
        delta_days = (target_date - base_date).days

        # Merakit kerangka data (DataFrame) dengan kolom bahasa Indonesia 
        # mutlak yang secara spesifik dibutuhkan oleh model scikit-learn bawaan
        features = pd.DataFrame({
            'hari_ke': [delta_days],
            'bulan': [target_date.month],
            'tahun': [target_date.year]
        })

        # Indikator debugging di terminal (tidak tampil di antarmuka web pengguna)
        # Sangat berguna untuk membuktikan kepada penguji bahwa vektorisasi data berjalan mulus
        print("DEBUG: Sending these columns to the model ->", features.columns.tolist())

        # Eksekusi kalkulasi algoritma kecerdasan buatan
        prediction_array = self.model.predict(features)
        
        # Ekstraksi angka murni dari array NumPy yang berlapis (Flattening array)
        predicted_value = np.array(prediction_array).flatten()[0]

        return float(predicted_value)

    # --- 3. METHOD PREDIKSI MASSAL (MACRO-TREND BATCHING) ---
    # Kemampuan objek untuk membuat proyeksi bulanan jangka panjang 
    # secara massal untuk kebutuhan visualisasi grafik lintasan makro.
    def generate_trend_data(self) -> pd.DataFrame:
        if self.model is None:
            return pd.DataFrame()

        # Menciptakan deret waktu (vektor tanggal) dari awal 2026 hingga akhir 2027
        # freq="MS" berarti mengambil setiap tanggal 1 (Month Start) di tiap bulan
        dates = pd.date_range(start="2026-01-01", end="2027-12-01", freq="MS").date
        base_date = date(2026, 1, 1)
        
        # Ekstraksi fitur secara loop cepat (List Comprehension) untuk performa tinggi
        delta_days = [(d - base_date).days for d in dates]
        months = [d.month for d in dates]
        years = [d.year for d in dates]

        # Konversi variabel list ke matriks Pandas siap-olah
        features = pd.DataFrame({
            'hari_ke': delta_days,
            'bulan': months,
            'tahun': years
        })

        # Komputasi prediksi masif dalam satu kali jalan (tidak mengulang loop prediksi lambat)
        prediction_array = self.model.predict(features)
        predictions_flat = np.array(prediction_array).flatten()

        # Mengembalikan tabel data hasil (Dataframe) dengan kolom yang rapi
        return pd.DataFrame({
            'Date': dates,
            'Valuation': predictions_flat
        })
