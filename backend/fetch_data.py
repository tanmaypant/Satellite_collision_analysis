import requests
import json
from datetime import datetime
import os 
import pandas as pd

def get_lat_lon(city_name):
    geocode_url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json"
    headers = {'User-Agent': 'satellite-collision-tracker/1.0'}
    response = requests.get(geocode_url, headers=headers)

    if response.status_code == 200 and response.json():
        data = response.json()[0]
        return float(data["lat"]), float(data["lon"])
    else:
        print("Location not found.")
        return None, None


API_KEY = "T32EAC-N9RRHY-R8EQ7B-5J8H"
ALT = 100
SECONDS = 60

# Folder path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
SAT_LIST_PATH = os.path.join(DATA_DIR, "satellite_list.json")

# Load satellite list
with open(SAT_LIST_PATH, "r") as f:
    data = json.load(f)

# Ask user for cities
city_names = input("Enter city names (comma-separated): ").split(",")

# Convert to location dicts
locations = []
for city in city_names:
    city = city.strip()
    lat, lon = get_lat_lon(city)
    if lat and lon:
        locations.append({"name": city, "lat": lat, "lon": lon})
    else:
        print(f"Skipping {city} due to missing coordinates.")


records= []

# Loop through each satellite
for sat in data["satellites"]:
    SAT_ID = sat["id"]
    SAT_NAME = sat.get("name", "Unknown")

    # Dictionary to hold all results for this satellite
    all_data = {
        "satellite_id": SAT_ID,
        "timestamp_utc": datetime.utcnow().isoformat(),
        "locations": []
    }

    # Fetch data for each location
    for loc in locations:
        url = f"https://api.n2yo.com/rest/v1/satellite/positions/{SAT_ID}/{loc['lat']}/{loc['lon']}/{ALT}/{SECONDS}?apiKey={API_KEY}"
        response = requests.get(url)

        if response.status_code == 200:
            sat_data = response.json()
            all_data["locations"].append({
                "name": loc["name"],
                "latitude": loc["lat"],
                "longitude": loc["lon"],
                "position_data": sat_data.get("positions", []),
                "info": sat_data.get("info", {})
            })
            for pos in sat_data.get("positions", []):
                records.append({
                    "location_name": loc["name"],
                    "latitude": loc["lat"],
                    "longitude": loc["lon"],
                    "satlatitude": pos.get("satlatitude"),
                    "satlongitude": pos.get("satlongitude"),
                    "sataltitude": pos.get("sataltitude"),
                    "azimuth": pos.get("azimuth"),
                    "elevation": pos.get("elevation"),
                    "ra": pos.get("ra"),
                    "dec": pos.get("dec"),
                    "eclipsed": pos.get("eclipsed"),
                    "timestamp": pos.get("timestamp"),
                    "satname": sat_data.get("info", {}).get("satname"),
                    "satid": sat_data.get("info", {}).get("satid")
                })
        else:
            print(f"Failed for {SAT_NAME} at {loc['name']}: {response.status_code}")
            all_data["locations"].append({
                "name": loc["name"],
                "latitude": loc["lat"],
                "longitude": loc["lon"],
                "error": f"{response.status_code} - {response.text}"
            })


if records:
    df = pd.DataFrame(records)
    csv_path = os.path.join(DATA_DIR, "test_data.csv")
    write_header = not os.path.isfile(csv_path) or os.path.getsize(csv_path) == 0
    df.to_csv(csv_path, mode='a', header=write_header, index=False)
    print(f"Saved CSV data to {csv_path}")
else:
    print("No valid data to save in CSV.")