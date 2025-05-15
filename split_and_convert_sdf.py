import os
import re
import subprocess

input_file = 'PubChem_compound_composite_query_Plasmodium falciparum IC50_records.sdf'
sdf_dir = 'split_sdf'
xyz_dir = 'xyz_files'

# Ensure directories exist
os.makedirs(sdf_dir, exist_ok=True)
os.makedirs(xyz_dir, exist_ok=True)

with open(input_file, 'r') as f:
    mol_lines = []
    for line in f:
        mol_lines.append(line)
        if line.strip() == "$$$$":
            mol_block = ''.join(mol_lines)
            match = re.search(r'> <PUBCHEM_COMPOUND_CID>\s*\n(\d+)', mol_block)
            if match:
                cid = match.group(1)
                sdf_path = os.path.join(sdf_dir, f'{cid}.sdf')
                xyz_path = os.path.join(xyz_dir, f'{cid}.xyz')
                # Write the SDF file
                with open(sdf_path, 'w') as sdf_file:
                    sdf_file.write(mol_block)
                # Convert to XYZ using Open Babel
                try:
                    subprocess.run(['obabel', sdf_path, '-O', xyz_path], check=True)
                    print(f"✅ Converted CID {cid} to XYZ format.")
                except subprocess.CalledProcessError:
                    print(f"❌ Conversion failed for CID {cid}")
            else:
                print("⚠️ No CID found in molecule. Skipping.")
            mol_lines = []

