import os
import joblib
import logging
import pandas as pd
import numpy as np

logger = logging.getLogger("UrbanIQ.ModelRegistry")

class ModelRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelRegistry, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.models = {}
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'models'))
        
        # 1. Population Model
        try:
            pop_path = os.path.join(base_path, 'population', 'population_density_model.joblib')
            self.models['population'] = joblib.load(pop_path)
            logger.info("Loaded population density model.")
        except Exception as e:
            logger.error(f"Failed to load population model: {e}")
            self.models['population'] = None

        # 2. Road Type Model
        try:
            road_path = os.path.join(base_path, 'roads', 'road_type_model.joblib')
            self.models['roads'] = joblib.load(road_path)
            logger.info("Loaded road type model.")
        except Exception as e:
            logger.error(f"Failed to load road type model: {e}")
            self.models['roads'] = None
            
        # 3. School Type Model
        try:
            school_path = os.path.join(base_path, 'schools', 'school_type_model.joblib')
            scaler_path = os.path.join(base_path, 'schools', 'scaler.joblib')
            self.models['schools_model'] = joblib.load(school_path)
            self.models['schools_scaler'] = joblib.load(scaler_path)
            logger.info("Loaded school type model & scaler.")
        except Exception as e:
            logger.error(f"Failed to load school models: {e}")
            self.models['schools_model'] = None

    def predict_population_density(self, lat: float, lon: float) -> dict:
        """Predict population density for a given lat/lon"""
        model = self.models.get('population')
        if not model:
            return {"status": "unavailable", "confidence": 0}
            
        CITY_CENTER_LAT = 31.5497
        CITY_CENTER_LON = 74.3436
        
        # Calculate features
        lat1, lon1, lat2, lon2 = map(np.radians, [lat, lon, CITY_CENTER_LAT, CITY_CENTER_LON])
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
        dist_to_center = 2 * 6371 * np.arcsin(np.sqrt(a))
        
        features = pd.DataFrame([{
            'longitude': lon,
            'latitude': lat,
            'dist_to_center_km': dist_to_center,
            'north_of_center': int(lat > CITY_CENTER_LAT),
            'east_of_center': int(lon > CITY_CENTER_LON),
            'lat_x_lon': lat * lon
        }])
        
        try:
            pred = model.predict(features)[0]
            return {
                "prediction": round(pred, 2),
                "model_version": "RF_v1",
                "status": "success",
                "confidence": 0.85 # Mocked for regression unless we have variance
            }
        except Exception as e:
            logger.error(f"Population prediction failed: {e}")
            return {"status": "error", "confidence": 0}

    def predict_road_type(self, road_name: str) -> dict:
        model = self.models.get('roads')
        if not model:
            return {"status": "unavailable", "confidence": 0}
            
        try:
            pred = model.predict([road_name])[0]
            # Since it's a pipeline with TFIDF and Classifier, we can try to get probabilities
            prob = 0.8 # default fallback
            if hasattr(model, "predict_proba"):
                probs = model.predict_proba([road_name])[0]
                prob = max(probs)
                
            return {
                "prediction": pred,
                "model_version": "Pipeline_v1",
                "status": "success",
                "confidence": round(float(prob), 2)
            }
        except Exception as e:
            logger.error(f"Road prediction failed: {e}")
            return {"status": "error", "confidence": 0}

# Global instance
registry = ModelRegistry()
