import pandas as pd
import numpy as np

print("=" * 60)
print("MERGING ALL DATA INTO MASTER DATASET")
print("=" * 60)

# ============================================
# 1. LOAD WEATHER DATA
# ============================================
print("\n📊 Loading Weather Data...")
df_weather = pd.read_csv('weather_data.csv')
df_weather['date'] = pd.to_datetime(df_weather['date'])
print(f"   Weather records: {len(df_weather)}")
print(f"   Date range: {df_weather['date'].min()} to {df_weather['date'].max()}")
print(f"   Columns: {df_weather.columns.tolist()}")

# ============================================
# 2. LOAD AIR QUALITY DATA
# ============================================
print("\n📊 Loading Air Quality Data...")
df_air = pd.read_csv('air_quality_data.csv')
df_air['date'] = pd.to_datetime(df_air['date']).dt.date  # Convert to date only
print(f"   AQ records: {len(df_air)}")
print(f"   Date range: {df_air['date'].min()} to {df_air['date'].max()}")
print(f"   Columns: {df_air.columns.tolist()}")

# ============================================
# 3. LOAD POPULATION DATA
# ============================================
print("\n📊 Loading Population Data...")
try:
    df_pop = pd.read_csv('population_data.csv')
    print(f"   Population points: {len(df_pop)}")
    print(f"   Average density: {df_pop['population_density'].mean():.2f} people/km²")
    
    # Calculate key population features
    avg_pop = df_pop['population_density'].mean()
    max_pop = df_pop['population_density'].max()
    min_pop = df_pop['population_density'].min()
    total_pop = df_pop['population_density'].sum()
    
except:
    print("   ⚠️ No population data found - using defaults")
    avg_pop = 5000  # Rough estimate for Lahore
    max_pop = 20000
    min_pop = 500
    total_pop = 11000000

# ============================================
# 4. LOAD SPATIAL DATA (Hospitals, Roads, etc.)
# ============================================
print("\n📊 Loading Spatial Data (OSM)...")
try:
    df_hospitals = pd.read_csv('hospitals_lahore.csv')
    num_hospitals = len(df_hospitals)
    print(f"   Hospitals: {num_hospitals}")
except:
    num_hospitals = 0
    print("   ⚠️ No hospital data found")

try:
    df_roads = pd.read_csv('roads_lahore.csv')
    num_roads = len(df_roads)
    print(f"   Roads: {num_roads}")
except:
    num_roads = 0
    print("   ⚠️ No road data found")

try:
    df_schools = pd.read_csv('schools_lahore.csv')
    num_schools = len(df_schools)
    print(f"   Schools: {num_schools}")
except:
    num_schools = 0
    print("   ⚠️ No school data found")

# ============================================
# 5. MERGE WEATHER + AIR QUALITY
# ============================================
print("\n🔄 Merging Weather and Air Quality...")

# Convert weather date to date only for merging
df_weather['date_only'] = df_weather['date'].dt.date

# Merge on date
df_merged = pd.merge(
    df_weather, 
    df_air, 
    left_on='date_only', 
    right_on='date', 
    how='inner'
)

print(f"   ✅ Merged records: {len(df_merged)}")
print(f"   Date range: {df_merged['date_only'].min()} to {df_merged['date_only'].max()}")

# ============================================
# 6. ADD POPULATION FEATURES
# ============================================
print("\n🔄 Adding Population Features...")

# Add population features to each row
df_merged['avg_population_density'] = avg_pop
df_merged['max_population_density'] = max_pop
df_merged['total_population'] = total_pop

# ============================================
# 7. ADD SPATIAL FEATURES
# ============================================
print("\n🔄 Adding Spatial Features...")

# Add infrastructure counts
df_merged['hospital_count'] = num_hospitals
df_merged['road_count'] = num_roads
df_merged['school_count'] = num_schools

# Calculate "infrastructure density" (per 100k people)
if total_pop > 0:
    df_merged['hospitals_per_100k'] = (num_hospitals / total_pop) * 100000
    df_merged['schools_per_100k'] = (num_schools / total_pop) * 100000
else:
    df_merged['hospitals_per_100k'] = 0
    df_merged['schools_per_100k'] = 0

# ============================================
# 8. CREATE RISK LABELS (for ML training)
# ============================================
print("\n🎯 Creating Risk Labels for ML Training...")

def calculate_risk(row):
    """
    Risk Score Calculation:
    - Temperature risk: 0-40 points
    - Air Quality risk: 0-40 points
    - Rainfall risk: 0-20 points
    """
    risk_score = 0
    
    # Temperature risk (check if column exists)
    if 'avg_temp_c' in row:
        temp = row['avg_temp_c']
        if temp >= 42:
            risk_score += 40
        elif temp >= 38:
            risk_score += 30
        elif temp >= 35:
            risk_score += 20
        elif temp >= 32:
            risk_score += 10
    
    # Air Quality risk (check if column exists)
    if 'pm25' in row:
        pm25 = row['pm25']
        if pm25 >= 200:
            risk_score += 40
        elif pm25 >= 150:
            risk_score += 30
        elif pm25 >= 100:
            risk_score += 20
        elif pm25 >= 50:
            risk_score += 10
    
    # Rainfall risk
    if 'total_rain_mm' in row:
        rain = row['total_rain_mm']
        if rain >= 50:
            risk_score += 20
        elif rain >= 25:
            risk_score += 10
    
    # Determine risk level
    if risk_score >= 60:
        return 2  # High Risk
    elif risk_score >= 30:
        return 1  # Moderate Risk
    else:
        return 0  # Low Risk

# Apply the risk calculation
df_merged['risk_level'] = df_merged.apply(calculate_risk, axis=1)

# Calculate actual risk score
def calculate_risk_score(row):
    score = 0
    
    if 'avg_temp_c' in row:
        temp = row['avg_temp_c']
        if temp >= 42: score += 40
        elif temp >= 38: score += 30
        elif temp >= 35: score += 20
        elif temp >= 32: score += 10
    
    if 'pm25' in row:
        pm25 = row['pm25']
        if pm25 >= 200: score += 40
        elif pm25 >= 150: score += 30
        elif pm25 >= 100: score += 20
        elif pm25 >= 50: score += 10
    
    if 'total_rain_mm' in row:
        rain = row['total_rain_mm']
        if rain >= 50: score += 20
        elif rain >= 25: score += 10
    
    return score

df_merged['risk_score'] = df_merged.apply(calculate_risk_score, axis=1)

# ============================================
# 9. CLEAN THE FINAL DATASET
# ============================================
print("\n🧹 Cleaning final dataset...")

# Drop unnecessary columns
columns_to_drop = ['date_only', 'date_y']
for col in columns_to_drop:
    if col in df_merged.columns:
        df_merged = df_merged.drop(columns=[col])

# Rename date column for consistency
if 'date_x' in df_merged.columns:
    df_merged = df_merged.rename(columns={'date_x': 'date'})

# Remove any rows with missing values
df_merged = df_merged.dropna()

# Convert date to string for clean CSV
df_merged['date'] = df_merged['date'].astype(str)

# ============================================
# 10. SAVE MASTER DATASET
# ============================================
print("\n💾 Saving Master Dataset...")
df_merged.to_csv('master_dataset.csv', index=False)

print(f"✅ MASTER DATASET CREATED SUCCESSFULLY!")
print(f"   Total records: {len(df_merged)}")
print(f"   Columns: {df_merged.columns.tolist()}")

# Show risk distribution
print(f"\n📈 Risk Level Distribution:")
print(df_merged['risk_level'].value_counts().sort_index())

# Show summary statistics
print("\n📊 Dataset Summary:")
print(f"   Date range: {df_merged['date'].min()} to {df_merged['date'].max()}")
if 'avg_temp_c' in df_merged.columns:
    print(f"   Average temperature: {df_merged['avg_temp_c'].mean():.2f}°C")
if 'pm25' in df_merged.columns:
    print(f"   Average PM2.5: {df_merged['pm25'].mean():.2f} μg/m³")
if 'avg_humidity_percent' in df_merged.columns:
    print(f"   Average humidity: {df_merged['avg_humidity_percent'].mean():.2f}%")

# Show first few rows
print("\n📋 First 5 rows:")
print(df_merged.head())

# Show correlation with risk
print("\n📊 Risk Distribution by Level:")
for level in [0, 1, 2]:
    count = len(df_merged[df_merged['risk_level'] == level])
    if count > 0:
        avg_temp = df_merged[df_merged['risk_level'] == level]['avg_temp_c'].mean() if 'avg_temp_c' in df_merged.columns else 0
        avg_pm25 = df_merged[df_merged['risk_level'] == level]['pm25'].mean() if 'pm25' in df_merged.columns else 0
        print(f"   Level {level}: {count} records | Avg Temp: {avg_temp:.1f}°C | Avg PM2.5: {avg_pm25:.1f}")

print("\n" + "=" * 60)
print("🎉 DATASET READY FOR ML TRAINING!")
print("=" * 60)