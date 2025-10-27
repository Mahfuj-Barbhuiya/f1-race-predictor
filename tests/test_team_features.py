import unittest
from src.feature_engineering.team_features import TeamFeatures
import pandas as pd

class TestTeamFeatures(unittest.TestCase):
    def setUp(self):
        self.results_df = pd.DataFrame({'constructor_id': ['x', 'x', 'x'], 'status': ['Finished', 'DNF', 'Finished']})
        self.df = TeamFeatures()
    def test_calculate_reliability_score(self):
        self.assertIsNone(self.df.calculate_reliability_score(self.results_df))
    def test_calculate_development_rate(self):
        self.assertIsNone(self.df.calculate_development_rate(self.results_df))
    def test_calculate_pit_stop_efficiency(self):
        self.assertIsNone(self.df.calculate_pit_stop_efficiency(self.results_df))
    def test_calculate_strategy_success_rate(self):
        self.assertIsNone(self.df.calculate_strategy_success_rate(self.results_df))

if __name__ == '__main__':
    unittest.main()
