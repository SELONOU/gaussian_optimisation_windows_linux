import os
import re
import pandas as pd
from pathlib import Path

def process_extxyz_file(file_path):
    file_name = file_path.stem
    with open(file_path, 'r') as file:
        lines = file.readlines()

    energies = []
    frame_indices = []
    frame_count = 0

    for line in lines:
        if line.startswith("Lattice="):
            match = re.search(r'energy=(-?\d+\.\d+)', line)
            if match:
                energy = float(match.group(1))
                energies.append(energy)
                frame_indices.append(f"{file_name}_frame_{frame_count:05d}")
                frame_count += 1

    if not energies:
        print(f"No energies found in {file_path.name}")
        return

    first_energy = energies[0]
    relative_energies = [energy - first_energy for energy in energies]

    df = pd.DataFrame({
        "frame_names": frame_indices,
        "Final_energy_frame_0": [first_energy] * len(energies),
        "State_Final_Energy": energies,
        "Relative_energy": relative_energies
    })

    output_csv = file_path.with_suffix('.csv')
    df.to_csv(output_csv, index=False)
    print(f"Processed {file_path.name} -> {output_csv.name}")

# Directory containing .extxyz files
directory = Path('.')  # You can change this to your specific path

# Process each .extxyz file
for extxyz_file in directory.glob("*.extxyz"):
    process_extxyz_file(extxyz_file)

