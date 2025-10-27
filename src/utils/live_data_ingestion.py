import random
import pandas as pd
import fastf1
from src.utils.f1_reference_data import DRIVER_NAMES, TEAM_NAMES

def build_driver_to_team(season=2025, event_name='Monaco', session_type='R'):
    try:
        session = fastf1.get_session(season, event_name, session_type)
        session.load()
        mapping = {}
        for drv in session.drivers:
            drv_info = session.get_driver(drv)
            # Find driver_id by name (reverse lookup)
            driver_id = None
            for k, v in DRIVER_NAMES.items():
                if v.lower() in drv_info['FullName'].lower():
                    driver_id = k
                    break
            # Find team_id by name (reverse lookup)
            team_id = None
            for k, v in TEAM_NAMES.items():
                if v.lower() in drv_info['TeamName'].lower():
                    team_id = k
                    break
            if driver_id and team_id:
                mapping[driver_id] = team_id
        return mapping
    except Exception as e:
        print(f"FastF1 mapping error: {e}. Using fallback mapping.")
        # Fallback to static mapping
        return {
            1: 1, 2: 2, 3: 3, 4: 4, 5: 3, 6: 2, 7: 1, 8: 5, 9: 4, 10: 6,
            11: 6, 12: 8, 13: 8, 14: 10, 15: 9, 16: 9, 17: 5, 18: 7, 19: 7, 20: 10
        }

DRIVER_TO_TEAM = build_driver_to_team()

class LiveDataIngestion:
    def get_latest_data(self):
        # Fetch real-time data for all drivers in the latest session
        try:
            session = fastf1.get_session(2025, 'Monaco', 'R')
            session.load()
            laps = session.laps.pick_fastest()  # Get fastest lap for each driver
            records = []
            for lap in laps.iterrows():
                lap_data = lap[1]
                driver_num = int(lap_data['DriverNumber'])
                driver_id = driver_num if driver_num in DRIVER_NAMES else 1
                constructor_id = DRIVER_TO_TEAM.get(driver_id, 1)
                grid_position = int(lap_data['GridPosition']) if 'GridPosition' in lap_data else 1
                lap_time = lap_data['LapTime'].total_seconds() if lap_data['LapTime'] else None
                fastest_lap = lap_time
                circuit_id = 5  # Monaco (example)
                records.append({
                    'season': 2025,
                    'round': 7,
                    'grid_position': grid_position,
                    'driver_id': driver_id,
                    'constructor_id': constructor_id,
                    'circuit_id': circuit_id,
                    'lap_time': lap_time,
                    'fastest_lap': fastest_lap
                })
            return pd.DataFrame(records)
        except Exception as e:
            print(f"FastF1 error: {e}. Using fallback random data.")
            # Fallback: simulate all drivers
            records = []
            for driver_id in range(1, 21):
                constructor_id = DRIVER_TO_TEAM.get(driver_id, 1)
                lap_time = round(random.uniform(75.0, 100.0), 3)
                fastest_lap = round(random.uniform(74.0, lap_time), 3)
                records.append({
                    'season': 2025,
                    'round': random.randint(1, 22),
                    'grid_position': random.randint(1, 20),
                    'driver_id': driver_id,
                    'constructor_id': constructor_id,
                    'circuit_id': random.randint(1, 25),
                    'lap_time': lap_time,
                    'fastest_lap': fastest_lap
                })
            return pd.DataFrame(records)
