import os
import json
import requests

def fetch_places(api_key, query, location, output_file):
    print(f"Fetching live data for '{query}'...")
    
    params = {
        "engine": "google_maps",
        "q": query,
        "ll": location,
        "api_key": api_key
    }
    
    # SerpApi endpoint
    url = "https://serpapi.com/search.json"
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        results = data.get("local_results", [])
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Save to JSON
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Successfully saved {len(results)} {query} to {output_file}")
        
    except Exception as e:
        print(f"❌ Error fetching data: {e}")

if __name__ == "__main__":
    # Replace with your actual SerpApi Key or set it as an environment variable
    API_KEY = os.environ.get("SERPAPI_KEY", "YOUR_ACTUAL_API_KEY")
    
    if API_KEY == "YOUR_ACTUAL_API_KEY":
        print("⚠️ WARNING: Please replace 'YOUR_ACTUAL_API_KEY' with your real SerpApi key.")
    
    # Lahore coordinates and zoom level
    LAHORE_COORDS = "@31.5204,74.3587,14z"
    
    # Fetch Hospitals
    fetch_places(
        api_key=API_KEY, 
        query="hospitals", 
        location=LAHORE_COORDS, 
        output_file=os.path.join(os.path.dirname(__file__), "..", "datasets", "live_hospitals.json")
    )
    
    # Fetch Schools
    fetch_places(
        api_key=API_KEY, 
        query="schools", 
        location=LAHORE_COORDS, 
        output_file=os.path.join(os.path.dirname(__file__), "..", "datasets", "live_schools.json")
    )
