# F1 Prediction Model Data Dictionary

## races
- race_id: Unique identifier for race
- season: Year of the race
- round: Race round in the season
- circuit_id: Track identifier
- race_name: Official race name
- race_date: Date of the race
- weather_conditions: Description of weather
- safety_cars: Number of safety car deployments
- red_flags: Number of red flags

## race_results
- result_id: Unique identifier for result
- race_id: Foreign key to races
- driver_id: Driver identifier
- constructor_id: Team identifier
- grid_position: Starting grid position
- final_position: Finishing position
- points: Points scored
- status: Race status (finished, DNF, etc.)
- laps_completed: Number of laps completed
- race_time: Total race time
- fastest_lap: Fastest lap time

## qualifying_results
- qual_id: Unique identifier for qualifying result
- race_id: Foreign key to races
- driver_id: Driver identifier
- constructor_id: Team identifier
- position: Qualifying position
- q1_time: Q1 session time
- q2_time: Q2 session time
- q3_time: Q3 session time
