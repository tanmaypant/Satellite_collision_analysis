import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import os 

# configurations
API_KEY="T32EAC-N9RRHY-R8EQ7B-5J8H"
SAT_ID="25544"  # ISS
LAT = 26.9154576
LON = 75.8189817
ALT= 0
SECONDS= 1

# Folder path
BASE_DIR= os.path.dirname(os.path.abspath(__file__))
DATA_DIR= os.path.join(BASE_DIR, "..", "data")

# URL
url = f"https://api.n2yo.com/rest/v1/satellite/positions/{SAT_ID}/{LAT}/{LON}/{ALT}/{SECONDS}?apiKey={API_KEY}"

# API REQUEST
response= requests.get(url)

if response.status_code== 200:
  data= response.json()

  # save JSON file
  json_path= os.path.join(DATA_DIR, "test_data.json")
  with open(json_path, "a") as json_file:
    json.dump(data, json_file, indent=4)
  print(f"Data saved to {json_path}")
else:
  print(f"Error: {response.status_code} - {response.text}")
  exit(1)