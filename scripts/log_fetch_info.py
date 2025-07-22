from datetime import datetime
import os

with open("./docs/fetch_log.txt", "a") as log:
    log.write(f"Data fetched at {datetime.now()} and saved to satellite_data.csv\n")
