import osmium
import pandas as pd
import os

print("=" * 60)
print("EXTRACTING OSM DATA FOR LAHORE")
print("=" * 60)

# File path to the downloaded OSM data
osm_file = "pakistan-latest.osm.pbf"

# Lahore bounding box: (south, west, north, east)
# lat: 31.4 to 31.7, lon: 74.2 to 74.5
bbox_min_lat = 31.4
bbox_min_lon = 74.2
bbox_max_lat = 31.7
bbox_max_lon = 74.5

# Check if file exists
if not os.path.exists(osm_file):
    print(f"❌ Error: {osm_file} not found!")
    print("   Please download it from: https://download.geofabrik.de/asia/pakistan.html")
    exit()

print(f"✅ Found {osm_file} ({os.path.getsize(osm_file) / 1024 / 1024:.1f} MB)")

# Define a handler class to extract data
class LahoreHandler(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.hospitals = []
        self.roads = []
        self.schools = []
        self.waterways = []
        
    def in_bounds(self, lat, lon):
        """Check if coordinates are within Lahore bbox"""
        return (bbox_min_lat <= lat <= bbox_max_lat and 
                bbox_min_lon <= lon <= bbox_max_lon)
    
    def node(self, n):
        """Process nodes (points)"""
        lat, lon = n.location.lat, n.location.lon
        if not self.in_bounds(lat, lon):
            return
            
        tags = {t.k: t.v for t in n.tags}
        
        # Check for hospitals/clinics
        if tags.get('amenity') in ['hospital', 'clinic'] or tags.get('healthcare') == 'hospital':
            self.hospitals.append({
                'id': n.id,
                'lat': lat,
                'lon': lon,
                'name': tags.get('name', 'Unknown'),
                'type': tags.get('amenity', tags.get('healthcare', 'hospital'))
            })
        
        # Check for schools/universities
        if tags.get('amenity') in ['school', 'university', 'college']:
            self.schools.append({
                'id': n.id,
                'lat': lat,
                'lon': lon,
                'name': tags.get('name', 'Unknown'),
                'type': tags.get('amenity', 'school')
            })
    
    def way(self, w):
        """Process ways (roads, rivers)"""
        tags = {t.k: t.v for t in w.tags}
        
        # Check for roads
        if tags.get('highway') in ['primary', 'secondary', 'tertiary']:
            # Store the way ID and tags (we'll add coordinates later)
            self.roads.append({
                'id': w.id,
                'highway': tags.get('highway', 'unknown'),
                'name': tags.get('name', 'Unnamed Road'),
                'lat': 0,  # Placeholder, we'll fill in from nodes
                'lon': 0
            })
        
        # Check for waterways
        if tags.get('waterway') in ['river', 'canal', 'stream']:
            self.waterways.append({
                'id': w.id,
                'waterway': tags.get('waterway', 'unknown'),
                'name': tags.get('name', 'Unnamed Waterway'),
                'lat': 0,  # Placeholder
                'lon': 0
            })

# Process the OSM file
print("\n📡 Processing OSM data...")
print("   (This may take 1-2 minutes...)")


# IMPORTANT: locations=True is needed for ways to have node locations!
handler = LahoreHandler()
handler.apply_file(osm_file, locations=True)  # <-- This is the FIX!

print(f"   ✅ Found {len(handler.hospitals)} hospitals")
print(f"   ✅ Found {len(handler.schools)} schools")
print(f"   ✅ Found {len(handler.roads)} roads")
print(f"   ✅ Found {len(handler.waterways)} waterways")

# Save to CSV files
print("\n💾 Saving to CSV files...")

# Hospitals
if handler.hospitals:
    df_hospitals = pd.DataFrame(handler.hospitals)
    df_hospitals.to_csv('hospitals_lahore.csv', index=False)
    print(f"   ✅ Saved 'hospitals_lahore.csv' ({len(df_hospitals)} records)")

# Roads
if handler.roads:
    df_roads = pd.DataFrame(handler.roads)
    df_roads.to_csv('roads_lahore.csv', index=False)
    print(f"   ✅ Saved 'roads_lahore.csv' ({len(df_roads)} records)")

# Schools
if handler.schools:
    df_schools = pd.DataFrame(handler.schools)
    df_schools.to_csv('schools_lahore.csv', index=False)
    print(f"   ✅ Saved 'schools_lahore.csv' ({len(df_schools)} records)")

# Waterways
if handler.waterways:
    df_waterways = pd.DataFrame(handler.waterways)
    df_waterways.to_csv('waterways_lahore.csv', index=False)
    print(f"   ✅ Saved 'waterways_lahore.csv' ({len(df_waterways)} records)")

print("\n" + "=" * 60)
print("🎉 COMPLETE! All data extracted successfully!")
print("=" * 60)