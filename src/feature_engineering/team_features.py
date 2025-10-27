import pandas as pd

class TeamFeatures:
    def calculate_reliability_score(self, results_df):
        # Calculate DNF rate for the team
        dnf_count = results_df[results_df['status'].str.contains('DNF|Retired|Accident|Mechanical', case=False)].shape[0]
        total = results_df.shape[0]
        reliability_score = 1 - (dnf_count / total) if total > 0 else None
        return reliability_score
    def calculate_development_rate(self, results_df):
        # For demo, difference in average points between first and last race
        if results_df.shape[0] < 2:
            return None
        first = results_df.iloc[0]['points']
        last = results_df.iloc[-1]['points']
        return last - first
    def calculate_pit_stop_efficiency(self, pit_stop_df):
        # For demo, mean pit stop time
        if 'pit_time' in pit_stop_df.columns:
            return pit_stop_df['pit_time'].mean()
        return None
    def calculate_strategy_success_rate(self, strategy_df):
        # For demo, percent of successful strategies
        if 'success' in strategy_df.columns:
            return strategy_df['success'].mean()
        return None
