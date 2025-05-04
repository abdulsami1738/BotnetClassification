import os
import json
from androguard.misc import AnalyzeAPK
from tqdm import tqdm

APK_ROOT_DIR = "Dataset"
OUTPUT_DIR = "Static_Features"  # Output folder for per-APK JSONs
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_static_features(apk_path):
    try:
        a, d, dx = AnalyzeAPK(apk_path)

        # External method calls
        methods = []
        if dx:
            for m in dx.get_methods():
                if m.is_external():
                    methods.append(m.name)

        # Safe intent filters
        intent_filters = []
        for activity in a.get_activities():
            filters = a.get_intent_filters("activity", activity)
            if filters:
                intent_filters.append({
                    "activity": activity,
                    "filters": list(filters.keys())
                })

        return {
            "apk_path": apk_path,
            "package_name": a.get_package(),
            "main_activity": a.get_main_activity(),
            "permissions": list(a.get_permissions()),
            "activities": list(a.get_activities()),
            "services": list(a.get_services()),
            "receivers": list(a.get_receivers()),
            "providers": list(a.get_providers()),
            "intent_filters": intent_filters,
            "api_methods": methods
        }

    except Exception as e:
        print(f"[ERROR] {apk_path}: {e}")
        return None

def process_all_apks(base_dir):
    for family in os.listdir(base_dir):
        family_path = os.path.join(base_dir, family)
        if not os.path.isdir(family_path):
            continue

        family_output_dir = os.path.join(OUTPUT_DIR, family)
        os.makedirs(family_output_dir, exist_ok=True)

        for apk_file in tqdm(os.listdir(family_path), desc=f"Processing {family}"):
            if not apk_file.endswith(".apk"):
                continue

            apk_path = os.path.join(family_path, apk_file)
            output_path = os.path.join(family_output_dir, apk_file.replace(".apk", ".json"))

            if os.path.exists(output_path):
                continue  # Skip if already processed

            result = extract_static_features(apk_path)
            if result:
                result["label"] = family
                with open(output_path, "w") as f:
                    json.dump(result, f, indent=2)

if __name__ == "__main__":
    process_all_apks(APK_ROOT_DIR)
    print("✅ Done extracting static features into individual JSON files.")
