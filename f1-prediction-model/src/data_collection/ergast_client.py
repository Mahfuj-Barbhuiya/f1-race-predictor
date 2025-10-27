import requests
import time
import functools
import os
import pickle

class ErgastAPIClient:
    BASE_URL = "https://ergast.com/api/f1/"
    CACHE_DIR = "src/data_collection/cache"
    RATE_LIMIT = 4  # max requests per second
    RETRY_LIMIT = 3
    RETRY_DELAY = 2

    def __init__(self):
        os.makedirs(self.CACHE_DIR, exist_ok=True)
        self.last_request_time = 0

    def _rate_limit(self):
        now = time.time()
        elapsed = now - self.last_request_time
        if elapsed < 1.0 / self.RATE_LIMIT:
            time.sleep(1.0 / self.RATE_LIMIT - elapsed)
        self.last_request_time = time.time()

    def _cache_path(self, key):
        return os.path.join(self.CACHE_DIR, f"{key}.pkl")

    def _get_cached(self, key):
        path = self._cache_path(key)
        if os.path.exists(path):
            with open(path, "rb") as f:
                return pickle.load(f)
        return None

    def _set_cache(self, key, value):
        path = self._cache_path(key)
        with open(path, "wb") as f:
            pickle.dump(value, f)

    def _request(self, endpoint):
        key = endpoint.replace('/', '_')
        cached = self._get_cached(key)
        if cached:
            return cached
        for attempt in range(self.RETRY_LIMIT):
            try:
                self._rate_limit()
                response = requests.get(self.BASE_URL + endpoint)
                response.raise_for_status()
                data = response.json()
                self._set_cache(key, data)
                return data
            except Exception as e:
                print(f"Error: {e}. Retrying {attempt+1}/{self.RETRY_LIMIT}...")
                time.sleep(self.RETRY_DELAY)
        raise Exception(f"Failed to fetch {endpoint} after {self.RETRY_LIMIT} attempts.")

    def get_races(self, season=None):
        endpoint = f"{season}.json" if season else "current.json"
        return self._request(endpoint)

    def get_results(self, season, round):
        endpoint = f"{season}/{round}/results.json"
        return self._request(endpoint)

    def get_qualifying(self, season, round):
        endpoint = f"{season}/{round}/qualifying.json"
        return self._request(endpoint)

    def get_drivers(self, season=None):
        endpoint = f"{season}/drivers.json" if season else "drivers.json"
        return self._request(endpoint)

    def get_constructors(self, season=None):
        endpoint = f"{season}/constructors.json" if season else "constructors.json"
        return self._request(endpoint)
