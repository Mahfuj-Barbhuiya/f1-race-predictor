"""
F1 Data Pipeline Script
- Cleans and processes raw race data
- Feature engineering for modeling
"""
import pandas as pd

import sqlite3
import json
import os

def preprocess_race_data(input_csv="raw_race_results.csv", output_csv="processed_race_data.csv"):
    df = pd.read_csv(input_csv)
    # Encode categorical features
    df['driver_id'] = df['driver'].astype('category').cat.codes
    df['constructor_id'] = df['constructor'].astype('category').cat.codes
    df['circuit_id'] = df['circuit'].astype('category').cat.codes
    # Target: Podium finish
    df['podium'] = (df['position'] <= 3).astype(int)
    features = ['season', 'round', 'grid', 'driver_id', 'constructor_id', 'circuit_id']
    df_out = df[features + ['podium']]
    df_out.to_csv(output_csv, index=False)
    print(f"Processed data saved to {output_csv}")

def load_sample_data_to_sqlite(json_path="f1-prediction-model/data/raw/sample_race_data.json", sqlite_path="data/processed/f1_data.sqlite"):
    """
    Loads sample race data from JSON and inserts into SQLite for offline development.
    """
    # Ensure output directory exists
    os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
    with open(json_path, "r") as f:
        data = json.load(f)
    # Flatten results
    rows = []
    for result in data["results"]:
        row = {
            "season": data["season"],
            "round": data["round"],
            "race_name": data["race_name"],
            "circuit_id": data["circuit_id"],
            "race_date": data["race_date"],
            "weather_conditions": data["weather_conditions"],
            "safety_cars": data["safety_cars"],
            "red_flags": data["red_flags"],
            "driver_id": result["driver_id"],
            "constructor_id": result["constructor_id"],
            "grid_position": result["grid_position"],
            "final_position": result["final_position"],
            "points": result["points"],
            "status": result["status"],
            "laps_completed": result["laps_completed"],
            "race_time": result["race_time"],
            "fastest_lap": result["fastest_lap"]
        }
        rows.append(row)
    # Create SQLite DB and table
    conn = sqlite3.connect(sqlite_path)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS race_results (
            season INTEGER,
            round INTEGER,
            race_name TEXT,
            circuit_id TEXT,
            race_date TEXT,
            weather_conditions TEXT,
            safety_cars INTEGER,
            red_flags INTEGER,
            driver_id TEXT,
            constructor_id TEXT,
            grid_position INTEGER,
            final_position INTEGER,
            points INTEGER,
            status TEXT,
            laps_completed INTEGER,
            race_time TEXT,
            fastest_lap TEXT
        )
    """)
    # Insert rows
    for row in rows:
        c.execute("""
            INSERT INTO race_results (
                season, round, race_name, circuit_id, race_date, weather_conditions, safety_cars, red_flags,
                driver_id, constructor_id, grid_position, final_position, points, status, laps_completed, race_time, fastest_lap
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, tuple(row.values()))
    conn.commit()
    conn.close()
    print(f"Sample data loaded into {sqlite_path}")


def export_sqlite_to_csv(sqlite_path="data/processed/f1_data.sqlite", output_csv="processed_race_data.csv"):
    """
    Export race_results table from SQLite to CSV for model training.
    """
    import pandas as pd
    conn = sqlite3.connect(sqlite_path)
    df = pd.read_sql_query("SELECT * FROM race_results", conn)
    # Encode categorical features
    df['driver_id'] = df['driver_id'].astype('category').cat.codes
    df['constructor_id'] = df['constructor_id'].astype('category').cat.codes
    df['circuit_id'] = df['circuit_id'].astype('category').cat.codes
    # Target: Podium finish
    df['podium'] = (df['final_position'] <= 3).astype(int)
    features = ['season', 'round', 'grid_position', 'driver_id', 'constructor_id', 'circuit_id']
    df_out = df[features + ['podium']]
    df_out.to_csv(output_csv, index=False)
    conn.close()
    print(f"Exported processed data to {output_csv}")

if __name__ == "__main__":
    import sys
    if "--load-sample-data" in sys.argv:
        load_sample_data_to_sqlite()
    elif "--export-csv" in sys.argv:
        export_sqlite_to_csv()
    else:
        preprocess_race_data()
