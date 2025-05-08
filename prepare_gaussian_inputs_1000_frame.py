import os
from glob import glob
from ase.io import read
from ase.io.gaussian import write_gaussian_in
import shutil

# Create output base directory
base_output_dir = "g16_inputs"
os.makedirs(base_output_dir, exist_ok=True)

# Create the new directory to store all .com files
molecules_g16_dir = "molecules_g16"
os.makedirs(molecules_g16_dir, exist_ok=True)

# Search for all extxyz files
extxyz_files = sorted(glob("*.extxyz"))

total_frames = 0

for xyz_file in extxyz_files:
    molecule_name = os.path.splitext(os.path.basename(xyz_file))[0]
    frames = read(xyz_file, index=":")

    for i, atoms in enumerate(frames):
        if i >= 1000:
            break  # Limit to first 1000 frames per molecule

        # Create directory for this molecule
        mol_dir = os.path.join(base_output_dir, molecule_name)
        os.makedirs(mol_dir, exist_ok=True)

        # Define output file path with updated naming convention
        com_path = os.path.join(mol_dir, f"{molecule_name}_frame_{i}.com")

        # Write the .com file correctly
        with open(com_path, "w") as f:
            # Write the header with the additional parameters
            f.write(f"%nprocshared=110\n")
            f.write(f"%mem=140GB\n")
            f.write(f"%NoSave\n")
            f.write(f"# wb97xd/6-311++G(3df,3pd)\n\n")

            # Write the molecule information
            f.write(f"Title for {molecule_name} frame {i}\n\n")
            f.write("0 1\n")  # Assuming charge=0 and multiplicity=1

            # Write the atom positions with 6 digits
            for atom in atoms:
                f.write(f"{atom.symbol} {atom.position[0]:.6f} {atom.position[1]:.6f} {atom.position[2]:.6f}\n")

            f.write("\n")

        # Move the generated .com file to the new directory
        shutil.move(com_path, os.path.join(molecules_g16_dir, f"{molecule_name}_frame_{i}.com"))

        total_frames += 1

print(f"✅ Wrote {total_frames} .com files (max 1000 per molecule) from {len(extxyz_files)} .extxyz files into '{molecules_g16_dir}/'")

