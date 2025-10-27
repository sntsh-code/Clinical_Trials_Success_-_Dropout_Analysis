import pandas as pd
import matplotlib.pyplot as plt
import os

# === Load dataset ===
file_path = r'C:\Users\USER\Documents\DATA ANALYST\PROJECTS\Resume Projects\Project 2 Clinical Success & Dropout Analysis\raw_data\clinical_trials_raw_data.xlsx'

if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found at: {file_path}")

df = pd.read_excel(file_path)

# Group and count trials by Phase and Study Status
phase_status_dist = df.groupby(['phases', 'study_status']).size().reset_index(name='trial_count')

# Sort by count for better visualization
phase_status_dist.sort_values(by='trial_count', ascending=False, inplace=True)

print("=== Trial Distribution by Phase and Status ===")
print(phase_status_dist)

# # === Save grouped summary (phase + status counts) ===
phase_status_path = r'C:\Users\USER\Documents\DATA ANALYST\PROJECTS\Resume Projects\Project 2 Clinical Success & Dropout Analysis\analysis\phase_status_distribution.xlsx'

with pd.ExcelWriter(phase_status_path, engine='openpyxl') as writer:
    # Grouped table
    phase_status_dist.to_excel(writer, index=False, sheet_name='Phase_Status_Counts')

print("Phase Status distribution saved at:")
print(phase_status_path)

# Pivot for a clearer table view
pivot_table = df.pivot_table(index='phases', columns='study_status', values='nct_number', aggfunc='count', fill_value=0)
print("\n=== Pivot Table View ===")
print(pivot_table)

# Visualization
pivot_table.plot(kind='bar', stacked=True, figsize=(12, 15))
plt.title('Clinical Trial Distribution by Phase and Status')
plt.xlabel('Trial Phase')
plt.ylabel('Number of Trials')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
