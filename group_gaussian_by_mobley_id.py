import os
import shutil
import re
from glob import glob

# Path to the directory containing all Gaussian input files
input_dir = "molecules_g16"
output_base_dir = "grouped_molecules"

# Make sure the output base directory exists
os.makedirs(output_base_dir, exist_ok=True)

# Get all .com files
com_files = glob(os.path.join(input_dir, "*.com"))

# Dictionary to group files by mobley number
mobley_groups = {}

# Process each file
for filepath in com_files:
    filename = os.path.basename(filepath)

    # Match pattern like mobley_5631798_nequip_...
    match = re.match(r"mobley_(\d+)_nequip_.*\.com", filename)
    if match:
        mobley_id = match.group(1)
        group_dir = os.path.join(output_base_dir, f"mobley_{mobley_id}")
        os.makedirs(group_dir, exist_ok=True)

        # Copy this file to the group directory
        shutil.copy(filepath, os.path.join(group_dir, filename))

print("✅ Done grouping files by mobley number into", output_base_dir)

