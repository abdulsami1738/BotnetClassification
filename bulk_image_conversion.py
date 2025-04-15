import os
import zipfile
import numpy as np
import math
from PIL import Image

def binary_to_image(binary_file, output_image):
    """
    Converts a binary file into a grayscale image where each byte is a pixel.

    :param binary_file: Path to the binary file (AndroidManifest.xml or classes.dex)
    :param output_image: Path to save the output image
    """
    with open(binary_file, "rb") as f:
        byte_data = f.read()

    pixel_values = np.frombuffer(byte_data, dtype=np.uint8)
    img_size = math.ceil(math.sqrt(len(pixel_values)))
    padded_size = img_size ** 2

    padded_pixels = np.pad(pixel_values, (0, padded_size - len(pixel_values)), mode='constant')
    image_array = padded_pixels.reshape((img_size, img_size))

    img = Image.fromarray(image_array, mode='L')
    img.save(output_image)
    print(f"Image saved: {output_image}")

def process_apks(apk_directory, output_directory):
    """
    Extracts AndroidManifest.xml from each APK in the given directory and converts it to an image.

    :param apk_directory: Directory containing APK files
    :param output_directory: Directory to save the extracted images
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for apk_file in os.listdir(apk_directory):
        if apk_file.endswith(".apk"):
            apk_path = os.path.join(apk_directory, apk_file)
            try:
                with zipfile.ZipFile(apk_path, 'r') as apk_zip:
                    manifest_name = "AndroidManifest.xml"
                    if manifest_name in apk_zip.namelist():
                        manifest_path = os.path.join(output_directory, f"{os.path.splitext(apk_file)[0]}.xml")
                        
                        # Extract AndroidManifest.xml
                        with apk_zip.open(manifest_name) as manifest_file, open(manifest_path, "wb") as output_file:
                            output_file.write(manifest_file.read())

                        # Convert to image
                        image_output_path = os.path.join(output_directory, f"{os.path.splitext(apk_file)[0]}.png")
                        binary_to_image(manifest_path, image_output_path)

                        # Cleanup extracted XML file
                        os.remove(manifest_path)

                    else:
                        print(f"AndroidManifest.xml not found in {apk_file}")

            except zipfile.BadZipFile:
                print(f"Invalid APK file: {apk_file}")

# Example usage:
output_dir = r"C:\Users\moham\OneDrive\Desktop\KFUPM\Courses\242\AML\Project\ImageDataset\Geinimi"
process_apks(r"C:\Users\moham\OneDrive\Desktop\KFUPM\Courses\242\AML\Project\Dataset\Geinimi", output_directory=output_dir)

output_dir = r"C:\Users\moham\OneDrive\Desktop\KFUPM\Courses\242\AML\Project\ImageDataset\MisoSMS"
process_apks(r"C:\Users\moham\OneDrive\Desktop\KFUPM\Courses\242\AML\Project\Dataset\MisoSMS", output_directory=output_dir)

output_dir = r"C:\Users\moham\OneDrive\Desktop\KFUPM\Courses\242\AML\Project\ImageDataset\Nickyspy"
process_apks(r"C:\Users\moham\OneDrive\Desktop\KFUPM\Courses\242\AML\Project\Dataset\Nickyspy", output_directory=output_dir)

# for NotCompatible
output_dir = r"C:\Users\moham\OneDrive\Desktop\KFUPM\Courses\242\AML\Project\ImageDataset\NotCompatible"
process_apks(r"C:\Users\moham\OneDrive\Desktop\KFUPM\Courses\242\AML\Project\Dataset\NotCompatible", output_directory=output_dir)

# for PJapps
output_dir = r"C:\Users\moham\OneDrive\Desktop\KFUPM\Courses\242\AML\Project\ImageDataset\PJapps"
process_apks(r"C:\Users\moham\OneDrive\Desktop\KFUPM\Courses\242\AML\Project\Dataset\PJapps", output_directory=output_dir)

# for Pletor
output_dir = r"C:\Users\moham\OneDrive\Desktop\KFUPM\Courses\242\AML\Project\ImageDataset\Pletor"
process_apks(r"C:\Users\moham\OneDrive\Desktop\KFUPM\Courses\242\AML\Project\Dataset\Pletor", output_directory=output_dir)

# for RootSmart
output_dir = r"C:\Users\moham\OneDrive\Desktop\KFUPM\Courses\242\AML\Project\ImageDataset\RootSmart"
process_apks(r"C:\Users\moham\OneDrive\Desktop\KFUPM\Courses\242\AML\Project\Dataset\RootSmart", output_directory=output_dir)

# for Sandroid
output_dir = r"C:\Users\moham\OneDrive\Desktop\KFUPM\Courses\242\AML\Project\ImageDataset\Sandroid"
process_apks(r"C:\Users\moham\OneDrive\Desktop\KFUPM\Courses\242\AML\Project\Dataset\Sandroid", output_directory=output_dir)

# for TigerBot
output_dir = r"C:\Users\moham\OneDrive\Desktop\KFUPM\Courses\242\AML\Project\ImageDataset\TigerBot"
process_apks(r"C:\Users\moham\OneDrive\Desktop\KFUPM\Courses\242\AML\Project\Dataset\TigerBot", output_directory=output_dir)

# for Wroba
output_dir = r"C:\Users\moham\OneDrive\Desktop\KFUPM\Courses\242\AML\Project\ImageDataset\Wroba"
process_apks(r"C:\Users\moham\OneDrive\Desktop\KFUPM\Courses\242\AML\Project\Dataset\Wroba", output_directory=output_dir)

# for Zitmo
output_dir = r"C:\Users\moham\OneDrive\Desktop\KFUPM\Courses\242\AML\Project\ImageDataset\Zitmo"
process_apks(r"C:\Users\moham\OneDrive\Desktop\KFUPM\Courses\242\AML\Project\Dataset\Zitmo", output_directory=output_dir)
