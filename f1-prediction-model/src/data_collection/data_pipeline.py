import sqlite3
from .ergast_client import ErgastAPIClient
from .fastf1_client import FastF1Client

class DataPipeline:
    def load_sample_data(self, sample_path="data/raw/sample_race_data.json"):
        import json
        with open(sample_path, "r") as f:
            data = json.load(f)
        race_id = f"{data['season']}_{data['round']}"
        self.conn.execute('''INSERT OR IGNORE INTO races (race_id, season, round, circuit_id, race_name, race_date, weather_conditions, safety_cars, red_flags) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (race_id, data['season'], data['round'], data['circuit_id'], data['race_name'], data['race_date'], data['weather_conditions'], data['safety_cars'], data['red_flags']))
        for result in data['results']:
            result_id = f"{race_id}_{result['driver_id']}"
            self.conn.execute('''INSERT OR IGNORE INTO race_results (result_id, race_id, driver_id, constructor_id, grid_position, final_position, points, status, laps_completed, race_time, fastest_lap) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (result_id, race_id, result['driver_id'], result['constructor_id'], result['grid_position'], result['final_position'], result['points'], result['status'], result['laps_completed'], result['race_time'], result['fastest_lap']))
        self.conn.commit()
    def __init__(self, db_path="data/processed/f1_data.sqlite"):
        self.db_path = db_path
        self.ergast = ErgastAPIClient()
        self.fastf1 = FastF1Client()
        self.conn = sqlite3.connect(self.db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS races (
            race_id TEXT PRIMARY KEY,
            season INTEGER,
            round INTEGER,
            circuit_id TEXT,
            race_name TEXT,
            race_date TEXT,
            weather_conditions TEXT,
            safety_cars INTEGER,
            red_flags INTEGER
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS race_results (
            result_id TEXT PRIMARY KEY,
            race_id TEXT,
            driver_id TEXT,
            constructor_id TEXT,
            grid_position INTEGER,
            final_position INTEGER,
            points REAL,
            status TEXT,
            laps_completed INTEGER,
            race_time TEXT,
            fastest_lap TEXT
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS qualifying_results (
            qual_id TEXT PRIMARY KEY,
            race_id TEXT,
            driver_id TEXT,
            constructor_id TEXT,
            position INTEGER,
            q1_time TEXT,
            q2_time TEXT,
            q3_time TEXT
        )''')
        self.conn.commit()

    def fetch_and_store_race_data(self, start_year=2014, end_year=2024):
        for year in range(start_year, end_year+1):
            races = self.ergast.get_races(year)
            for race in races['MRData']['RaceTable']['Races']:
                race_id = f"{year}_{race['round']}"
                circuit_id = race['Circuit']['circuitId']
                race_name = race['raceName']
                race_date = race['date']
                # Weather, safety cars, red flags: placeholder
                weather_conditions = 'Unknown'
                safety_cars = 0
                red_flags = 0
                self.conn.execute('''INSERT OR IGNORE INTO races (race_id, season, round, circuit_id, race_name, race_date, weather_conditions, safety_cars, red_flags) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (race_id, year, race['round'], circuit_id, race_name, race_date, weather_conditions, safety_cars, red_flags))
                # Results
                results = self.ergast.get_results(year, race['round'])
                for result in results['MRData']['RaceTable']['Races'][0]['Results']:
                    result_id = f"{race_id}_{result['Driver']['driverId']}"
                    driver_id = result['Driver']['driverId']
                    constructor_id = result['Constructor']['constructorId']
                    grid_position = int(result['grid'])
                    final_position = int(result['position'])
                    points = float(result['points'])
                    status = result['status']
                    laps_completed = int(result['laps'])
                    race_time = result.get('Time', {}).get('time', None)
                    fastest_lap = result.get('FastestLap', {}).get('Time', None)
                    self.conn.execute('''INSERT OR IGNORE INTO race_results (result_id, race_id, driver_id, constructor_id, grid_position, final_position, points, status, laps_completed, race_time, fastest_lap) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        (result_id, race_id, driver_id, constructor_id, grid_position, final_position, points, status, laps_completed, race_time, fastest_lap))
                # Qualifying
                qual = self.ergast.get_qualifying(year, race['round'])
                for qresult in qual['MRData']['RaceTable']['Races'][0]['QualifyingResults']:
                    qual_id = f"{race_id}_{qresult['Driver']['driverId']}"
                    driver_id = qresult['Driver']['driverId']
                    constructor_id = qresult['Constructor']['constructorId']
                    position = int(qresult['position'])
                    q1_time = qresult.get('Q1', None)
                    q2_time = qresult.get('Q2', None)
                    q3_time = qresult.get('Q3', None)
                    self.conn.execute('''INSERT OR IGNORE INTO qualifying_results (qual_id, race_id, driver_id, constructor_id, position, q1_time, q2_time, q3_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                        (qual_id, race_id, driver_id, constructor_id, position, q1_time, q2_time, q3_time))
        self.conn.commit()

    # Add more methods for data collection, validation, and storage
