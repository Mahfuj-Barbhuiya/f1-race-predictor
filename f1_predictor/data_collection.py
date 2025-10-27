"""
F1 Data Collection Script
- Collects race, driver, and constructor data from the Ergast API
- Saves raw data as CSV for further processing
"""
import requests
import pandas as pd
import time

def fetch_race_results(start_year=2018, end_year=2024):
    all_races = []
    for year in range(start_year, end_year+1):
        url = f"https://ergast.com/api/f1/{year}/results.json?limit=1000"
        print(f"Fetching {year} data from {url}")
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            races = resp.json().get('MRData', {}).get('RaceTable', {}).get('Races', [])
            if not races:
                print(f"No races found for {year}!")
            for race in races:
                for result in race['Results']:
                    all_races.append({
                        'season': year,
                        'round': race['round'],
                        'raceName': race['raceName'],
                        'circuit': race['Circuit']['circuitName'],
                        'driver': result['Driver']['familyName'],
                        'constructor': result['Constructor']['name'],
                        'grid': int(result['grid']),
                        'position': int(result['position']),
                        'status': result['status'],
                        'points': float(result['points'])
                    })
        except Exception as e:
            print(f"Error fetching data for {year}: {e}")
        time.sleep(0.5)  # Be polite to the API
    if not all_races:
        print("No race data collected! Check API or network.")
    return pd.DataFrame(all_races)

if __name__ == "__main__":
    df = fetch_race_results()
    if not df.empty:
        df.to_csv("f1_predictor/raw_race_results.csv", index=False)
        print(f"Saved {len(df)} race results to f1_predictor/raw_race_results.csv")
    else:
        print("No data to save. Exiting.")
