import pandas as pd
import math
from datetime import datetime
import os

INPUT_FILE = "./data/clean_data.csv"
LOG_FILE = "./logs/proximity_alerts.log"
MIN_SAFE_DISTANCE_KM = 10  # You can adjust this threshold

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def log_event(message):
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"[{datetime.now()}] {message}\n")

# Load and clean
df = pd.read_csv(INPUT_FILE)
df = df.dropna(subset=['satlatitude', 'satlongitude'])

# Drop exact duplicate positions
df = df[['satname', 'satlatitude', 'satlongitude']].drop_duplicates().reset_index(drop=True)

# Compare all unique pairs
for i in range(len(df)):
    for j in range(i + 1, len(df)):
        sat1 = df.iloc[i]
        sat2 = df.iloc[j]

        dist = haversine_distance(sat1['satlatitude'], sat1['satlongitude'], sat2['satlatitude'], sat2['satlongitude'])

        if dist < MIN_SAFE_DISTANCE_KM:
            warning = (
                f" WARNING: {sat1['satname']} and {sat2['satname']} are {dist:.2f} km apart!"
            )
            print(warning)
            log_event(warning)
