import os
import re

input_file = 'PubChem_compound_composite_query_Plasmodium falciparum IC50_records.sdf'
output_dir = 'split_sdf'

os.makedirs(output_dir, exist_ok=True)

with open(input_file, 'r') as f:
    mol_lines = []
    for line in f:
        mol_lines.append(line)
        if line.strip() == "$$$$":
            # Convert block to string for CID extraction
            mol_block = ''.join(mol_lines)
            # Extract CID using regex
            match = re.search(r'> <PUBCHEM_COMPOUND_CID>\s*\n(\d+)', mol_block)
            if match:
                cid = match.group(1)
                filename = os.path.join(output_dir, f'{cid}.sdf')
                with open(filename, 'w') as out:
                    out.write(mol_block)
                print(f"Saved molecule with CID {cid} to {filename}")
            else:
                print("⚠️ CID not found in one molecule. Skipping.")
            mol_lines = []  # Reset for next molecule

