import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.model_registry import registry as model_registry

def test_population_model():
    # Near center of Lahore
    res = model_registry.predict_population_density(31.55, 74.34)
    if res["status"] == "success":
        assert "prediction" in res
        assert res["prediction"] > 0
        assert "confidence" in res
        assert "model_version" in res

def test_road_model():
    res = model_registry.predict_road_type("Ferozepur Road")
    if res["status"] == "success":
        assert "prediction" in res
        assert res["prediction"] in ['primary', 'secondary', 'tertiary']
        assert "confidence" in res
