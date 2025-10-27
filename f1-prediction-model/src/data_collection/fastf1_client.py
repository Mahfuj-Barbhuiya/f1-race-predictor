import fastf1
import os
import logging

class FastF1Client:
    def __init__(self, cache_dir="src/data_collection/fastf1_cache"):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)
        fastf1.Cache.enable_cache(self.cache_dir)
        logging.basicConfig(level=logging.INFO)

    def get_session(self, year, event_name, session_type):
        try:
            session = fastf1.get_session(year, event_name, session_type)
            session.load()
            return session
        except Exception as e:
            logging.error(f"Session not found or error loading: {year} {event_name} {session_type}: {e}")
            return None

    def get_telemetry(self, year, event_name, session_type, driver):
        session = self.get_session(year, event_name, session_type)
        if session is None:
            return None
        try:
            laps = session.laps.pick_driver(driver)
            telemetry = laps.get_car_data()
            return telemetry
        except Exception as e:
            logging.error(f"Error extracting telemetry for {driver}: {e}")
            return None

    def get_all_drivers(self, year, event_name, session_type):
        session = self.get_session(year, event_name, session_type)
        if session is None:
            return []
        return session.drivers
