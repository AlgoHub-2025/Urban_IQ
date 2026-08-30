import requests
import pandas as pd
import time
from datetime import datetime, timedelta

print("=" * 60)
print("FETCHING AIR QUALITY DATA FROM AQICN")
print("=" * 60)

# Your AQICN Token (from your email)
AQICN_TOKEN = "487cde8fe5a1da57a7907818b8ac0c270f9847d0"

# Step 1: Fetch CURRENT air quality for Lahore
print("\n📡 Fetching current air quality for Lahore...")

url = "https://api.waqi.info/feed/lahore/"
params = {"token": AQICN_TOKEN}

try:
    response = requests.get(url, params=params)
    data = response.json()
    
    if data['status'] == 'ok':
        aqi_data = data['data']
        print(f"✅ Current AQI: {aqi_data['aqi']}")
        print(f"   Location: {aqi_data['city']['name']}")
        print(f"   Time: {aqi_data['time']['s']}")
        
        # Extract PM2.5
        pm25 = aqi_data['iaqi'].get('pm25', {}).get('v', 0)
        pm10 = aqi_data['iaqi'].get('pm10', {}).get('v', 0)
        print(f"   PM2.5: {pm25} μg/m³")
        print(f"   PM10: {pm10} μg/m³")
        
        # Save current data
        current_data = {
            'date': [datetime.now().date()],
            'pm25': [pm25],
            'pm10': [pm10],
            'aqi': [aqi_data['aqi']]
        }
        df_current = pd.DataFrame(current_data)
        df_current.to_csv('air_quality_current.csv', index=False)
        print("✅ Saved current data to 'air_quality_current.csv'")
        
    else:
        print(f"❌ Error: {data}")
        
except Exception as e:
    print(f"❌ Exception: {e}")

# Step 2: Fetch FORECAST data (next 5 days)
print("\n📡 Fetching forecast data for next 5 days...")

forecast_url = "https://api.waqi.info/feed/lahore/"
forecast_params = {"token": AQICN_TOKEN}

try:
    response = requests.get(forecast_url, params=forecast_params)
    data = response.json()
    
    if data['status'] == 'ok':
        aqi_data = data['data']
        
        # Get forecast for PM2.5
        if 'forecast' in aqi_data and 'daily' in aqi_data['forecast']:
            pm25_forecast = aqi_data['forecast']['daily'].get('pm25', [])
            pm10_forecast = aqi_data['forecast']['daily'].get('pm10', [])
            
            print(f"✅ Found forecast data for {len(pm25_forecast)} days")
            
            # Create forecast dataframe
            forecast_dates = []
            forecast_pm25 = []
            forecast_pm10 = []
            
            for day in pm25_forecast:
                forecast_dates.append(day['day'])
                forecast_pm25.append(day['avg'])
            
            for day in pm10_forecast:
                forecast_pm10.append(day['avg'])
            
            # Create DataFrame
            df_forecast = pd.DataFrame({
                'date': forecast_dates,
                'pm25_forecast': forecast_pm25,
                'pm10_forecast': forecast_pm10[:len(forecast_dates)]  # Match length
            })
            
            df_forecast.to_csv('air_quality_forecast.csv', index=False)
            print("✅ Saved forecast data to 'air_quality_forecast.csv'")
            print("\nForecast for next 5 days:")
            print(df_forecast)
        
except Exception as e:
    print(f"❌ Exception fetching forecast: {e}")

# Step 3: Build a HISTORICAL dataset by fetching over time
# Since AQICN free tier doesn't provide historical data directly,
# we'll create a "mock" historical dataset based on current conditions
# This is for training your ML model

print("\n📊 Building training dataset...")
print("   (Note: For real historical data, you'd need to fetch this every hour)")

# Create synthetic historical data based on current conditions
# This is a placeholder - in production you'd fetch real historical data
today = datetime.now().date()
historical_dates = []
historical_pm25 = []
historical_pm10 = []
historical_temp = []
historical_humidity = []

# Generate 365 days of data (based on current conditions + seasonal variation)
for i in range(365):
    date = today - timedelta(days=i)
    historical_dates.append(date)
    
    # Seasonal variation (winter has higher pollution in Lahore)
    month = date.month
    if month in [11, 12, 1, 2]:  # Winter months
        seasonal_factor = 1.5  # Higher pollution
    elif month in [6, 7, 8]:  # Monsoon
        seasonal_factor = 0.7  # Lower pollution
    else:
        seasonal_factor = 1.0
    
    # Base PM2.5 + variation
    base_pm25 = 80 + (50 * seasonal_factor)
    variation = (i * 7) % 30 - 15  # Some variation
    pm25_value = max(10, base_pm25 + variation)
    
    base_pm10 = 120 + (60 * seasonal_factor)
    pm10_value = max(20, base_pm10 + variation)
    
    # Temperature (Lahore: hot summers, mild winters)
    if month in [5, 6, 7, 8]:  # Summer
        temp = 35 + (i % 10)
    elif month in [11, 12, 1]:  # Winter
        temp = 15 + (i % 8)
    else:
        temp = 25 + (i % 10)
    
    # Humidity
    humidity = 40 + (i % 40)
    
    historical_pm25.append(pm25_value)
    historical_pm10.append(pm10_value)
    historical_temp.append(temp)
    historical_humidity.append(humidity)

# Create DataFrame
df_historical = pd.DataFrame({
    'date': historical_dates,
    'pm25': historical_pm25,
    'pm10': historical_pm10,
    'temperature': historical_temp,
    'humidity': historical_humidity
})

# Sort by date (oldest first)
df_historical = df_historical.sort_values('date')

# Save to CSV
df_historical.to_csv('air_quality_data.csv', index=False)
print(f"✅ Saved {len(df_historical)} records to 'air_quality_data.csv'")
print("\nFirst 5 rows:")
print(df_historical.head())
print("\nLast 5 rows:")
print(df_historical.tail())

print("\n" + "=" * 60)
print("🎉 COMPLETE! You now have:")
print("  - air_quality_current.csv (Real-time data)")
print("  - air_quality_forecast.csv (5-day forecast)")
print("  - air_quality_data.csv (Training dataset)")
print("=" * 60)