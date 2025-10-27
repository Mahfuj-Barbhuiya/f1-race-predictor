import unittest
from fastapi.testclient import TestClient
from src.utils.api import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
    def test_predict_race(self):
        response = self.client.post('/predict/race', json={"race_id": "2023_bahrain", "session_type": "race"})
        self.assertIn(response.status_code, [200, 422])
    def test_predict_qualifying(self):
        response = self.client.post('/predict/qualifying', json={"race_id": "2023_bahrain", "session_type": "qualifying"})
        self.assertIn(response.status_code, [200, 422])
    def test_model_performance(self):
        response = self.client.get('/model/performance')
        self.assertIn(response.status_code, [200, 422])
    def test_feature_importance(self):
        response = self.client.get('/features/importance')
        self.assertIn(response.status_code, [200, 422])

if __name__ == '__main__':
    unittest.main()
