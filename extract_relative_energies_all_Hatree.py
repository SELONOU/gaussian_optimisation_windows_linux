import os
import re
import pandas as pd
from pathlib import Path

# Conversion factor: 1 Hartree = 627.5095 kcal/mol
HARTREE_TO_KCAL_MOL = 627.5095

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

    # Convert energies from Hartree to kcal/mol
    energies_kcal_mol = [energy * HARTREE_TO_KCAL_MOL for energy in energies]
    first_energy_kcal_mol = energies_kcal_mol[0]

    # Compute relative energies in kcal/mol
    relative_energies_kcal_mol = [energy - first_energy_kcal_mol for energy in energies_kcal_mol]

    # Create DataFrame with energies in kcal/mol
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
directory = Path('.')  # You can change this to your specific path

# Process each .extxyz file
for extxyz_file in directory.glob("*.extxyz"):
    process_extxyz_file(extxyz_file)

