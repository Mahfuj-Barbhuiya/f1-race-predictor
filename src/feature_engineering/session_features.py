import pandas as pd

class SessionFeatures:
    def calculate_practice_pace(self, session_df):
        # For demo, mean lap time
        if 'lap_time' in session_df.columns:
            return session_df['lap_time'].mean()
        return None
    def calculate_tire_degradation(self, stint_df):
        # For demo, difference between first and last lap time
        if 'lap_time' in stint_df.columns and stint_df.shape[0] > 1:
            return stint_df.iloc[-1]['lap_time'] - stint_df.iloc[0]['lap_time']
        return None
    def calculate_relative_performance(self, session_df):
        # For demo, gap to median lap time
        if 'lap_time' in session_df.columns:
            median = session_df['lap_time'].median()
            session_df['gap_to_median'] = session_df['lap_time'] - median
            return session_df
        return session_df
    def extract_sector_performance(self, sector_df):
        # For demo, sum of sector times
        if {'sector1', 'sector2', 'sector3'}.issubset(sector_df.columns):
            sector_df['total_sector_time'] = sector_df['sector1'] + sector_df['sector2'] + sector_df['sector3']
            return sector_df
        return sector_df
