"""
F1 Model Training Script
- Trains a baseline XGBoost model to predict podium finishes
"""

import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os


def train_podium_model(input_csv="processed_race_data.csv", model_path="trained_podium_model.joblib"):
    df = pd.read_csv(input_csv)
    X = df.drop('podium', axis=1)
    y = df['podium']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = XGBClassifier(n_estimators=200, max_depth=6, learning_rate=0.1, use_label_encoder=False, eval_metric='logloss')
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    # Save model
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
    return model

if __name__ == "__main__":
    train_podium_model()
