from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

app = FastAPI(title="F1 Prediction API")


import pandas as pd
import os
from datetime import datetime
import joblib

MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../trained_podium_model.joblib"))
PROCESSED_CSV = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../processed_race_data.csv"))
MODEL_VERSION = "0.1-xgb"
if os.path.exists(PROCESSED_CSV):
    df = pd.read_csv(PROCESSED_CSV)
else:
    df = pd.DataFrame()
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None

class PredictionRequest(BaseModel):
    race_id: str
    session_type: str  # 'qualifying', 'race'
    include_probabilities: bool = False

class PredictionResponse(BaseModel):
    predictions: List[Dict]
    confidence_scores: Optional[List[float]]
    model_version: str
    generated_at: datetime

@app.post("/predict/race")
async def predict_race(request: PredictionRequest):
    # Use trained model for predictions
    if df.empty or model is None:
        raise HTTPException(status_code=500, detail="No data/model available.")
    # For demo, predict on all rows and return top 3 predicted podiums
    X = df.drop('podium', axis=1)
    y_pred = model.predict_proba(X)[:, 1]  # Probability of podium
    df['podium_proba'] = y_pred
    preds = df.sort_values("podium_proba", ascending=False).head(3)
    predictions = preds.to_dict(orient="records")
    return PredictionResponse(
        predictions=predictions,
        confidence_scores=list(preds['podium_proba']),
        model_version=MODEL_VERSION,
        generated_at=datetime.utcnow()
    )

@app.post("/predict/qualifying")
async def predict_qualifying(request: PredictionRequest):
    # Use trained model for predictions (same as race for demo)
    if df.empty or model is None:
        raise HTTPException(status_code=500, detail="No data/model available.")
    X = df.drop('podium', axis=1)
    y_pred = model.predict_proba(X)[:, 1]
    df['podium_proba'] = y_pred
    preds = df.sort_values("podium_proba", ascending=False).head(3)
    predictions = preds.to_dict(orient="records")
    return PredictionResponse(
        predictions=predictions,
        confidence_scores=list(preds['podium_proba']),
        model_version=MODEL_VERSION,
        generated_at=datetime.utcnow()
    )

@app.get("/model/performance")
async def get_model_performance():
    # Dummy metrics
    return {
        "accuracy": 0.85,
        "precision": 0.8,
        "recall": 0.78,
        "f1": 0.79,
        "model_version": MODEL_VERSION
    }

@app.get("/features/importance")
async def get_feature_importance():
    # Dummy feature importances
    return {
        "feature_importance": {
            "grid_position": 0.4,
            "driver_id": 0.2,
            "constructor_id": 0.15,
            "season": 0.1,
            "round": 0.1,
            "circuit_id": 0.05
        },
        "model_version": MODEL_VERSION
    }
