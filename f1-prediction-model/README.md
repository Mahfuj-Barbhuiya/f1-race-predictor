# F1 Prediction Model

A comprehensive Formula 1 race prediction system that forecasts race outcomes, qualifying positions, and provides probability distributions for various scenarios.

## Project Structure
- **data/**: Raw, processed, and feature datasets
- **src/**: Source code modules
- **notebooks/**: Jupyter notebooks for analysis and EDA
- **configs/**: Configuration files
- **tests/**: Unit and integration tests
- **docs/**: Documentation

## Setup
1. Create and activate the Python virtual environment:
   ```powershell
   python -m venv f1_prediction_env
   .\f1_prediction_env\Scripts\activate
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Configure project parameters in `configs/config.yaml`.

## Goals
- Predict race and qualifying outcomes
- Provide probability distributions for scenarios
- Integrate multiple data sources (APIs, web scraping)
- Develop robust, production-ready ML models

## Documentation
See `docs/` for technical and user documentation.

## Testing
Set the `PYTHONPATH` and run tests:
```powershell
$env:PYTHONPATH="C:\Users\barbh\PROJECT"
pytest --maxfail=5 --disable-warnings
```
