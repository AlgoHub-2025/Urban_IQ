import rasterio
import pandas as pd
import numpy as np

print("=" * 60)
print("PROCESSING POPULATION DATA (WorldPop)")
print("=" * 60)

# Open the downloaded raster file
try:
    with rasterio.open('population.tif') as src:
        # Read the data (single band)
        data = src.read(1)
        
        # Get the bounding box coordinates
        bounds = src.bounds
        print(f"✅ Successfully opened population.tif")
        print(f"   Bounds: {bounds}")
        print(f"   Resolution: {src.res}")
        
        # Get the transform (how to convert pixel coords to lat/lon)
        transform = src.transform
        
        # Create arrays of latitudes and longitudes for each pixel
        rows, cols = data.shape
        print(f"   Grid size: {rows} rows x {cols} columns")
        
        # Generate coordinate arrays
        # For each row, the longitude is the same, for each column, latitude is same
        # We'll use the transform to get actual coordinates
        import numpy as np
        
        # Get all pixel coordinates
        # This is memory-intensive for large files, so we'll sample or aggregate
        # For 1km resolution Pakistan file, this should be manageable
        
        # Get the coordinates for each pixel center
        # Instead of getting every single pixel (millions), let's aggregate
        
        # Extract only the Lahore region (bounding box: 31.4-31.7 lat, 74.2-74.5 lon)
        # First, find the pixel indices for Lahore
        # We'll use the transform to convert lat/lon to pixel coordinates
        from rasterio.transform import rowcol
        
        # Lahore bounding box
        lon_min, lon_max = 74.2, 74.5
        lat_min, lat_max = 31.4, 31.7
        
        # Convert to pixel coordinates
        row_start, col_start = rowcol(transform, lon_min, lat_max)  # top-left
        row_end, col_end = rowcol(transform, lon_max, lat_min)  # bottom-right
        
        # Ensure we have valid indices
        row_start = max(0, min(rows-1, row_start))
        row_end = max(0, min(rows-1, row_end))
        col_start = max(0, min(cols-1, col_start))
        col_end = max(0, min(cols-1, col_end))
        
        print(f"   Extracting Lahore region: rows {row_start}-{row_end}, cols {col_start}-{col_end}")
        
        # Extract the Lahore data
        lahore_data = data[row_start:row_end+1, col_start:col_end+1]
        
        # Get the actual lat/lon for each pixel in the Lahore region
        # We'll create arrays of coordinates
        # Get the transform for the extracted region
        from rasterio.transform import Affine
        
        # Get coordinates for each pixel
        # We'll use numpy meshgrid
        # First, get the x (longitude) and y (latitude) for each pixel
        x_coords = np.arange(col_start, col_end+1)
        y_coords = np.arange(row_start, row_end+1)
        
        # Convert pixel indices to actual coordinates
        xs = []
        ys = []
        for row in y_coords:
            for col in x_coords:
                x, y = transform * (col, row)
                xs.append(x)
                ys.append(y)
        
        # Flatten the population data
        pop_values = lahore_data.flatten()
        
        # Create DataFrame
        df_pop = pd.DataFrame({
            'longitude': xs,
            'latitude': ys,
            'population_density': pop_values
        })
        
        # Remove invalid values (-99999 is common for no data)
        df_pop = df_pop[df_pop['population_density'] > 0]
        
        # Round coordinates to 4 decimal places (about 11m precision)
        df_pop['longitude'] = df_pop['longitude'].round(4)
        df_pop['latitude'] = df_pop['latitude'].round(4)
        
        # Save to CSV
        df_pop.to_csv('population_data.csv', index=False)
        print(f"✅ Successfully saved {len(df_pop)} population records to 'population_data.csv'")
        
        # Show summary
        print(f"\n📊 Population Summary for Lahore:")
        print(f"   Total population in area: {df_pop['population_density'].sum():,.0f}")
        print(f"   Average density: {df_pop['population_density'].mean():.2f} people/km²")
        print(f"   Max density: {df_pop['population_density'].max():.2f} people/km²")
        print(f"   Min density: {df_pop['population_density'].min():.2f} people/km²")
        
        # Show first few rows
        print(f"\nFirst 5 rows:")
        print(df_pop.head())
        
except FileNotFoundError:
    print("❌ ERROR: File 'population.tif' not found!")
    print("\nPlease download it from:")
    print("https://data.humdata.org/dataset/worldpop-population-density-for-pakistan")
    print("Then rename it to 'population.tif' and put it in this folder.")
    
except Exception as e:
    print(f"❌ Exception: {e}")
    print("\n💡 If you don't have rasterio installed, run:")
    print("   pip install rasterio")