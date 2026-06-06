import pickle
import numpy as np
import pandas as pd
from datetime import date

class GoldPredictor:
    def __init__(self, model_path: str):
        self.model_path = model_path
        try:
            with open(self.model_path, 'rb') as file:
                self.model = pickle.load(file)
        except FileNotFoundError:
            self.model = None

    def predict(self, target_date: date) -> float:
        if self.model is None:
            return 0.0

        if target_date.year not in [2026, 2027]:
            raise ValueError("G-Ture currently only projects for the 2026-2027 horizon.")

        base_date = date(2026, 1, 1)
        delta_days = (target_date - base_date).days

        # Our strict Indonesian columns
        features = pd.DataFrame({
            'hari_ke': [delta_days],
            'bulan': [target_date.month],
            'tahun': [target_date.year]
        })

        # This will print to your terminal so we know the new code is running!
        print("DEBUG: Sending these columns to the model ->", features.columns.tolist())

        prediction_array = self.model.predict(features)
        predicted_value = np.array(prediction_array).flatten()[0]

        return float(predicted_value)

    def generate_trend_data(self) -> pd.DataFrame:
        if self.model is None:
            return pd.DataFrame()

        dates = pd.date_range(start="2026-01-01", end="2027-12-01", freq="MS").date
        base_date = date(2026, 1, 1)
        
        delta_days = [(d - base_date).days for d in dates]
        months = [d.month for d in dates]
        years = [d.year for d in dates]

        features = pd.DataFrame({
            'hari_ke': delta_days,
            'bulan': months,
            'tahun': years
        })

        prediction_array = self.model.predict(features)
        predictions_flat = np.array(prediction_array).flatten()

        return pd.DataFrame({
            'Date': dates,
            'Valuation': predictions_flat
        })