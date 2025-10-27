import pandas as pd

class BaselineModels:
    def last_race_position(self, results_df):
        # Predict same position as last race
        pass
    def season_average_position(self, results_df):
        # Predict based on season average
        pass
    def qualifying_position_model(self, qualifying_df):
        # Race position = qualifying position
        pass
    def betting_odds_model(self, odds_df):
        # Convert betting odds to probabilities
        pass
