import os
import re
import pandas as pd
from pathlib import Path

# Conversion factor: 1 eV = 23.0609 kcal/mol
EV_TO_KCAL_MOL = 23.0609

def process_extxyz_file(file_path, max_frames=1000):
    file_name = file_path.stem
    with open(file_path, 'r') as file:
        lines = file.readlines()

    energies = []
    frame_indices = []
    frame_count = 0
    line_index = 0

    while line_index < len(lines) and frame_count < max_frames:
        if lines[line_index].startswith("Lattice="):
            match = re.search(r'energy=(-?\d+\.\d+)', lines[line_index])
            if match:
                energy = float(match.group(1))
                energies.append(energy)
                frame_indices.append(f"{file_name}_frame_{frame_count:05d}")
                frame_count += 1
        line_index += 1

    if not energies:
        print(f"No energies found in {file_path.name}")
        return

    # Convert energies from eV to kcal/mol
    energies_kcal_mol = [energy * EV_TO_KCAL_MOL for energy in energies]
    first_energy_kcal_mol = energies_kcal_mol[0]

    # Compute relative energies in kcal/mol
    relative_energies_kcal_mol = [energy - first_energy_kcal_mol for energy in energies_kcal_mol]

    # Create DataFrame
    df = pd.DataFrame({
        "frame_names": frame_indices,
        "Final_energy_frame_0": [first_energy_kcal_mol] * len(energies_kcal_mol),  # Initial energy in kcal/mol
        "State_Final_Energy": energies_kcal_mol,  # All energies in kcal/mol
        "Relative_energy": relative_energies_kcal_mol  # Relative energies in kcal/mol
    })

    # Save DataFrame to CSV
    output_csv = file_path.with_suffix('.csv')
    df.to_csv(output_csv, index=False)
    print(f"Processed {file_path.name} -> {output_csv.name}")

# Directory containing .extxyz files
directory = Path('.')  # You can change this path if needed

# Process each .extxyz file (limit to first 1000 frames)
for extxyz_file in directory.glob("*.extxyz"):
    process_extxyz_file(extxyz_file, max_frames=1000)

