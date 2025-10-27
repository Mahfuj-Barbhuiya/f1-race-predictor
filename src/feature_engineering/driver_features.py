import pandas as pd

class DriverFeatures:
    def calculate_elo_rating(self, results_df):
        # Simple ELO rating based on position
        elo = 1500
        ratings = []
        for _, row in results_df.iterrows():
            change = (11 - row['final_position']) * 10
            elo += change
            ratings.append(elo)
        results_df['elo_rating'] = ratings
        return results_df
    def calculate_form_metrics(self, results_df, window_sizes=[3, 5, 10]):
        for window in window_sizes:
            results_df[f'form_avg_pos_{window}'] = results_df['final_position'].rolling(window).mean()
            results_df[f'form_avg_pts_{window}'] = results_df['points'].rolling(window).mean()
        return results_df
    def calculate_consistency_score(self, results_df):
        results_df['consistency_score'] = results_df['final_position'].rolling(5).std()
        return results_df
    def calculate_track_affinity(self, results_df, track_type):
        # For demo, just return mean position
        affinity = results_df['final_position'].mean()
        return affinity
    def calculate_h2h_records(self, results_df, vs_driver):
        # For demo, just return 0 (no driver_id in live data)
        return 0
