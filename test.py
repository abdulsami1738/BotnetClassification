# function to remove all corrupt files in a directory

import os
import zipfile
import numpy as np
import math

# Function to remove all corrupt files in a directory without opening them
def remove_corrupt_files(directory):
    """
    Removes all corrupt files in the given directory.
    
    :param directory: Directory containing files to check
    """
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            try:
                with open(file_path, "rb") as f:
                    byte_data = f.read()
                    np.frombuffer(byte_data, dtype=np.uint8)
            except Exception as e:
                print(f"Corrupt file: {file_path}")
                os.remove(file_path)

# Example usage
remove_corrupt_files(r"Dataset")

