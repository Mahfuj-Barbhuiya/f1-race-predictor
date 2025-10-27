import pandas as pd
class PredictionService:
    def __init__(self, model):
        self.model = model
    def preprocess(self, df):
        # Drop non-numeric columns, fill NA, encode if needed
        df = df.select_dtypes(include=['number', 'bool', 'category'])
        # Drop lap_time and fastest_lap if present
        for col in ['lap_time', 'fastest_lap']:
            if col in df.columns:
                df = df.drop(columns=[col])
        df = df.fillna(0)
        return df
    def predict(self, race_data):
        try:
            X = self.preprocess(race_data)
            pred = self.model.predict(X)
            return pred.tolist()
        except Exception as e:
            return f'Prediction error: {e}'
