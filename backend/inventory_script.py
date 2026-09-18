import joblib
import os
import glob
from pprint import pformat

def inspect_models():
    model_files = glob.glob("e:/Lahore HackaThone/models/**/*.joblib", recursive=True)
    report = []
    
    for f in model_files:
        try:
            model = joblib.load(f)
            type_name = type(model).__name__
            attributes = []
            
            if hasattr(model, 'feature_names_in_'):
                attributes.append(f"Features expected: {list(model.feature_names_in_)}")
            if hasattr(model, 'classes_'):
                attributes.append(f"Classes: {list(model.classes_)}")
            
            report.append(f"### {os.path.basename(f)}\n- **Path:** {f}\n- **Type:** {type_name}\n- **Info:** {', '.join(attributes) if attributes else 'No explicit feature_names_in_'}")
            
        except Exception as e:
            report.append(f"### {os.path.basename(f)}\n- **Path:** {f}\n- **Error loading:** {e}")
            
    with open("e:/Lahore HackaThone/backend/model_inventory.md", "w") as out:
        out.write("# Model Artifact Inventory\n\n" + "\n\n".join(report))

if __name__ == "__main__":
    inspect_models()
