import unittest
from src.feature_engineering.session_features import SessionFeatures
import pandas as pd

class TestSessionFeatures(unittest.TestCase):
    def setUp(self):
        self.session_df = pd.DataFrame({'lap_time': [90, 91, 92]})
        self.sf = SessionFeatures()
    def test_calculate_practice_pace(self):
        self.assertIsNone(self.sf.calculate_practice_pace(self.session_df))
    def test_calculate_tire_degradation(self):
        self.assertIsNone(self.sf.calculate_tire_degradation(self.session_df))
    def test_calculate_relative_performance(self):
        self.assertIsNone(self.sf.calculate_relative_performance(self.session_df))
    def test_extract_sector_performance(self):
        self.assertIsNone(self.sf.extract_sector_performance(self.session_df))

if __name__ == '__main__':
    unittest.main()
