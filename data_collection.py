import requests
import pandas as pd
import time
from datetime import datetime

# YOUR CONFIG
API_TOKEN = "....."
LAT = "27.1567"
LON = "84.9978"
CSV_FILE = "simara_live_log.csv"

def fetch_and_save():
    url = f"https://api.waqi.info/feed/geo:{LAT};{LON}/?token={API_TOKEN}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data['status'] == 'ok':
            result = data['data']
            row = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'aqi': result.get('aqi'),
                'pm25': result.get('iaqi', {}).get('pm25', {}).get('v'),
                'temp': result.get('iaqi', {}).get('t', {}).get('v'),
                'humidity': result.get('iaqi', {}).get('h', {}).get('v')
            }
            
            # Save to CSV (append mode)
            df = pd.DataFrame([row])
            df.to_csv(CSV_FILE, mode='a', header=not pd.io.common.file_exists(CSV_FILE), index=False)
            print(f"[{row['timestamp']}] Data logged for Simara. AQI: {row['aqi']}")
            
    except Exception as e:
        print(f"Error: {e}")

print("🚀 Starting Hourly Logger... Press Ctrl+C to stop.")
while True:
    fetch_and_save()
    # Wait for 1 hour (3600 seconds)
    time.sleep(3600)
