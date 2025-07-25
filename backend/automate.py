import json
import time
import subprocess
from datetime import datetime
import os

SATELLITE_LIST = "./data/satellite_list.json"
LOG_FILE = "./logs/alerts.log"
FETCH_INTERVAL = 60  # seconds (every minute)

def log_event(message):
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"[{datetime.now()}] {message}\n")

def load_satellite_ids():
    with open(SATELLITE_LIST, "r") as f:
        data = json.load(f)
        return [sat["id"] for sat in data["satellites"]]

def run_script(script_name):
    full_path = os.path.join(os.path.dirname(__file__), script_name)
    result = subprocess.run(["python", full_path], capture_output=True, text=True)

    if result.returncode != 0:
        log_event(f"❌ Error in {script_name}:\n{result.stderr}")
    else:
        log_event(f"✅ Successfully ran {script_name}")

if __name__ == "__main__":
    log_event("🚀 Starting Satellite Collision Monitor Automation")
    
    while True:
        try:
            log_event("🔄 New cycle started.")

            # Step 1: Fetch data
            run_script("fetch_data.py")

            # Step 2: Clean data
            run_script("clean_data.py")

            # Step 3: Calculate proximity
            run_script("calculate_proximity.py")

            log_event("✅ Cycle completed. Sleeping...\n")
            time.sleep(FETCH_INTERVAL)

        except KeyboardInterrupt:
            log_event("🛑 Automation stopped by user.")
            break

        except Exception as e:
            log_event(f"❗ Unexpected Error: {str(e)}")
            time.sleep(60)
