import pandas as pd
import numpy as np
from datetime import datetime, timedelta


FILENAME = "simara_1year_hourly.csv"
HOURS_IN_YEAR = 8760
START_DATE = datetime.now() - timedelta(days=365)

def generate_simara_history():
    data = []
    
    for i in range(HOURS_IN_YEAR):
        current_time = START_DATE + timedelta(hours=i)
        month = current_time.month
        hour = current_time.hour
        
        # 1. Seasonal Baseline
        if month in [3, 4, 5]:    # Pre-Monsoon (Dust & Fires)
            base_pm25 = 140
        elif month in [6, 7, 8]:  # Monsoon (Rain cleans air)
            base_pm25 = 35
        elif month in [11, 12, 1]: # Winter (Inversion)
            base_pm25 = 110
        else:                     # Post-Monsoon
            base_pm25 = 75
            
        # 2. Hourly Patterns 
        # We use a sine wave to simulate the daily cycle
        daily_cycle = 25 * np.sin(2 * np.pi * (hour - 6) / 24)
        
        # 3. Add Random "Noise" (Weather fluctuations)
        noise = np.random.normal(0, 15)
        
        # Final PM2.5 Calculation
        pm25 = max(5, base_pm25 + daily_cycle + noise)
        
        # 4. Convert PM2.5 to AQI 
        if pm25 <= 12: aqi = (50/12) * pm25
        elif pm25 <= 35: aqi = ((100-51)/(35-12.1)) * (pm25-12.1) + 51
        else: aqi = ((200-151)/(150-55)) * (pm25-55) + 151
        
        data.append([current_time, round(pm25, 2), int(aqi)])

    df = pd.DataFrame(data, columns=['Timestamp', 'PM25', 'AQI'])
    df.to_csv(FILENAME, index=False)
    print(f"✅ Created {FILENAME} with {len(df)} hourly records!")

if __name__ == "__main__":
    generate_simara_history()
