import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from flask import Flask, request, jsonify
from joblib import load
from src.utils.prediction_service import PredictionService

app = Flask(__name__)
model = load('trained_podium_model.joblib')
predictor = PredictionService(model)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    # Expecting a dict with keys matching model features
    import pandas as pd
    df = pd.DataFrame([data])
    prediction = predictor.predict(df)
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
