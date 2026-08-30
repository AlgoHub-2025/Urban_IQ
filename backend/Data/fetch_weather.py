import requests
import pandas as pd

print("Fetching Weather Data...")

url = "https://archive-api.open-meteo.com/v1/archive"

# Correct parameters for Lahore
params = {
    "latitude": 31.5497,
    "longitude": 74.3436,
    "start_date": "2020-01-01",
    "end_date": "2024-12-31",
    "daily": ["temperature_2m_mean", "relative_humidity_2m_mean", "precipitation_sum", "wind_speed_10m_max"],
    "timezone": "Asia/Karachi"
}

# CRITICAL FIX: Add params=params to the request!
response = requests.get(url, params=params)

# Check if it worked
if response.status_code == 200:
    data = response.json()['daily']
    df_weather = pd.DataFrame(data)
    
    # Clean the columns to make it ML-ready
    df_weather.columns = ['date', 'avg_temp_c', 'avg_humidity_percent', 'total_rain_mm', 'max_wind_kmh']
    df_weather['date'] = pd.to_datetime(df_weather['date'])
    
    # Save to CSV
    df_weather.to_csv('weather_data.csv', index=False)
    print(f"✅ Successfully saved {len(df_weather)} days of weather data to 'weather_data.csv'")
else:
    print(f"❌ Error: {response.status_code} - {response.text}")
