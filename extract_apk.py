import zipfile
import os

def extract_dex_manifest(apk_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with zipfile.ZipFile(apk_path, 'r') as apk:
        for file_name in apk.namelist():
            # if file_name in {"classes.dex", "AndroidManifest.xml"}:
                apk.extract(file_name, output_dir)
                print(f"Extracted: {file_name}")

# Example usage
apk_file = r"C:\Users\moham\Downloads\Compressed\Adware\Adware\587908c9947094fe5be83116c356fcef85b1f0b474b865b8ca414c53254d944d.65c6b25d6c848eb7e3bc733f9c64ae5c"
output_directory = r"C:\Users\moham\OneDrive\Desktop\KFUPM\Courses\242\AML\Project\Dataset\extracted_files"
extract_dex_manifest(apk_file, output_directory)
