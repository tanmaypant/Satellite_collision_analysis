import pandas as pd
from datetime import datetime

# Load the data
df = pd.read_csv("./data/test_data.csv")

# Drop rows only if critical columns are missing
df.dropna(subset=['location_name', 'latitude', 'longitude', 'satlatitude', 'satlongitude', 'sataltitude', 'timestamp'], inplace=True)

# Drop any duplicate rows
df.drop_duplicates(inplace=True)

# Convert UNIX timestamp to readable format (if you have time or launch data)
if 'timestamp' in df.columns:
    df['readable_time'] = df['timestamp'].apply(lambda ts: datetime.fromtimestamp(ts))

# Drop unnecessary columns (example)
columns_to_drop = ['azimuth','elevation','ra', 'dec','eclipsed']
df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True)

# Save cleaned data
df.to_csv("./data/clean_data.csv", index=False)

# Log the clean
with open("./docs/fetch_log.txt", "w") as log:
    log.write(f"Cleaned data on {datetime.now()} – Rows: {len(df)}\n")

print("Data cleaned and saved. :)")