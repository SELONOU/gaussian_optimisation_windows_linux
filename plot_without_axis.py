import pandas as pd
import matplotlib.pyplot as plt
import os
import re

# File path (update this if needed)
csv_file = 'relative_energies_ML_QM_mobley_2661134.csv'

# Read the CSV data
df = pd.read_csv(csv_file)

# Updated columns based on your CSV
frame_col = 'frame number'  # Frame number
qm_col = 'E (rel.en.kcal/mol of QM)'  # QM relative energy
ml_col = 'Relative_energy'  # ML relative energy

# Extract only the last digits after 'frame_' and pad to 4 digits
df['Frame_Display'] = df[frame_col].apply(
    lambda x: re.search(r'frame_([0-9]+)', str(x)).group(1).zfill(4) if re.search(r'frame_([0-9]+)', str(x)) else str(x)
)

# Plot with clear background and no grid
fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')
ax.plot(df['Frame_Display'], df[qm_col], label='QM Relative Energy (kcal/mol)', color='blue')
ax.plot(df['Frame_Display'], df[ml_col], label='ML Relative Energy (kcal/mol)', color='red')

# Labels and title
ax.set_xlabel('Frame Number')
ax.set_ylabel('Relative Energy (kcal/mol)')
ax.set_title('Relative Energies: QM vs ML')
ax.legend(frameon=False)

# Improve x-axis: show fewer ticks, rotate labels for clarity
ax.set_xticks(df['Frame_Display'][::max(1, len(df)//15)])
ax.tick_params(axis='x', rotation=45, labelsize=8)

# Remove grid and spines
ax.grid(False)
for spine in ax.spines.values():
    spine.set_visible(False)

# Save the plot in the same directory as the CSV
output_file = os.path.splitext(csv_file)[0] + '_plot.png'
plt.savefig(output_file, bbox_inches='tight', facecolor='white')

print(f"Plot saved as: {output_file}")

