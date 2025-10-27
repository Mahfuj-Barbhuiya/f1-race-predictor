import sqlite3
import pandas as pd
from src.feature_engineering.driver_features import DriverFeatures
from src.feature_engineering.team_features import TeamFeatures
from src.feature_engineering.session_features import SessionFeatures

# Load sample race results from database
conn = sqlite3.connect('data/processed/f1_data.sqlite')
race_results = pd.read_sql_query('SELECT * FROM race_results', conn)
conn.close()

# Driver features
df = DriverFeatures()
race_results = df.calculate_elo_rating(race_results)
race_results = df.calculate_form_metrics(race_results)
race_results = df.calculate_consistency_score(race_results)
track_affinity = df.calculate_track_affinity(race_results, 'street')
h2h = df.calculate_h2h_records(race_results, race_results['driver_id'].iloc[0])

# Team features
tf = TeamFeatures()
reliability = tf.calculate_reliability_score(race_results)
development = tf.calculate_development_rate(race_results)

# Session features (using race_results as dummy session_df)
sf = SessionFeatures()
practice_pace = sf.calculate_practice_pace(race_results)
tire_degradation = sf.calculate_tire_degradation(race_results)
relative_perf = sf.calculate_relative_performance(race_results)

print('Driver features:', race_results.head())
print('Track affinity:', track_affinity)
print('H2H:', h2h)
print('Team reliability:', reliability)
print('Team development:', development)
print('Practice pace:', practice_pace)
print('Tire degradation:', tire_degradation)
print('Relative performance:', relative_perf.head())
