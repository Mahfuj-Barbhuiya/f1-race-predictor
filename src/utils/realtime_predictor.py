import time
import threading
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.utils.live_data_ingestion import LiveDataIngestion
from src.utils.prediction_service import PredictionService
from src.utils.model_monitor import ModelMonitor
from src.utils.alerting_system import AlertingSystem
from src.utils.f1_reference_data import DRIVER_NAMES, TEAM_NAMES, TRACK_NAMES
from joblib import load

# Load trained model
MODEL_PATH = 'trained_podium_model.joblib'
model = load(MODEL_PATH)

# Initialize services
live_data = LiveDataIngestion()
predictor = PredictionService(model)
monitor = ModelMonitor()
alerter = AlertingSystem()

def run_realtime_predictor():
    print('Starting real-time race predictor...')
    while True:
        race_data = live_data.get_latest_data()
        if race_data is not None:
            predictions = predictor.predict(race_data)
            results = []
            for i, row in race_data.iterrows():
                driver_name = DRIVER_NAMES.get(row['driver_id'], f"ID {row['driver_id']}")
                team_name = TEAM_NAMES.get(row['constructor_id'], f"ID {row['constructor_id']}")
                pos = row['grid_position']
                lap_time_sec = row.get('lap_time', None)
                if lap_time_sec is not None and lap_time_sec != 'N/A':
                    minutes = int(lap_time_sec // 60)
                    seconds = lap_time_sec % 60
                    lap_time = f"{minutes}:{seconds:06.3f}"
                else:
                    lap_time = 'N/A'
                pred = predictions[i] if isinstance(predictions, (list, tuple)) else predictions
                results.append((pred, driver_name, team_name, pos, lap_time))
            # Sort by predicted position (ascending)
            results.sort(key=lambda x: x[0])
            for pos, (pred, driver_name, team_name, grid_pos, lap_time) in enumerate(results, 1):
                print(f"{pos:<4}{driver_name:<20}{team_name:<15}{grid_pos:<6}{lap_time:<10}{pred:<10}")
            print('-------------------------------\n')
            monitor.track(predictions, race_data)
            if monitor.needs_alert():
                alerter.send_alert('Model anomaly detected!')
        time.sleep(5)
        global latest_results_df
        latest_results_df = pd.DataFrame()
        print('Starting real-time race predictor...')
        while True:
            race_data = live_data.get_latest_data()
            if race_data is not None:
                predictions = predictor.predict(race_data)
                results = []
                for i, row in race_data.iterrows():
                    driver_name = DRIVER_NAMES.get(row['driver_id'], f"ID {row['driver_id']}")
                    team_name = TEAM_NAMES.get(row['constructor_id'], f"ID {row['constructor_id']}")
                    pos = row['grid_position']
                    lap_time_sec = row.get('lap_time', None)
                    if lap_time_sec is not None and lap_time_sec != 'N/A':
                        minutes = int(lap_time_sec // 60)
                        seconds = lap_time_sec % 60
                        lap_time = f"{minutes}:{seconds:06.3f}"
                    else:
                        lap_time = 'N/A'
                    pred = predictions[i] if isinstance(predictions, (list, tuple)) else predictions
                    results.append({
                        'Pos': pos,
                        'Driver': driver_name,
                        'Team': team_name,
                        'LapTime': lap_time,
                        'Prediction': pred
                    })
                # Sort by predicted position (ascending)
                results.sort(key=lambda x: x['Prediction'])
                latest_results_df = pd.DataFrame(results)
                print('\n--- Real-Time Race Predictions ---')
                print(f"Track: {TRACK_NAMES.get(race_data.iloc[0]['circuit_id'], 'Unknown')}")
                print(f"Season: {race_data.iloc[0]['season']} | Round: {race_data.iloc[0]['round']}")
                print(latest_results_df.to_string(index=False))
                # Export to CSV
                csv_name = f"race_predictions_{race_data.iloc[0]['season']}_{race_data.iloc[0]['round']}.csv"
                latest_results_df.to_csv(csv_name, index=False)
                print(f"Results exported to {csv_name}")
                monitor.track(predictions, race_data)
                if monitor.needs_alert():
                    alerter.send_alert('Model anomaly detected!')
            time.sleep(5)

    # Flask dashboard
    app = Flask(__name__)

    @app.route('/')
    def dashboard():
        global latest_results_df
        if latest_results_df.empty:
            return '<h2>No predictions yet. Please wait...</h2>'
        table_html = latest_results_df.to_html(index=False)
        return render_template_string(f"<h2>Live F1 Race Predictions</h2>{table_html}")

    def run_dashboard():
        app.run(port=8080)

    if __name__ == '__main__':
        threading.Thread(target=run_realtime_predictor, daemon=True).start()
        run_dashboard()

if __name__ == '__main__':
    threading.Thread(target=run_realtime_predictor).start()
