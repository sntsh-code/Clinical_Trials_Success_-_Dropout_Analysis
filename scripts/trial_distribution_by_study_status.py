import pandas as pd
import matplotlib.pyplot as plt
import os

# === Load dataset ===
file_path = r'C:\Users\USER\Documents\DATA ANALYST\PROJECTS\Resume Projects\Project 2 Clinical Success & Dropout Analysis\clean_data\clinical_trials_clean_data.xlsx'

if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found at: {file_path}")

df = pd.read_excel(file_path)
# === 1. Group and count trials by Study Status ===
study_status_dist = df.groupby(['study_status']).size().reset_index(name='trial_count')
study_status_dist.sort_values(by='trial_count', ascending=False, inplace=True)

print("=== Trial Distribution by Study Status ===")
print(study_status_dist)

# === 2. Save grouped summary ===
study_status_path = r'C:\Users\USER\Documents\DATA ANALYST\PROJECTS\Resume Projects\Project 2 Clinical Success & Dropout Analysis\analysis\study_status_distribution.xlsx'

with pd.ExcelWriter(study_status_path, engine='openpyxl') as writer:
    study_status_dist.to_excel(writer, index=False, sheet_name='Study_Status_Counts')

print("Study Status distribution saved at:")
print(study_status_path)

# === 3. Pivot Table (for visualization) ===
pivot_table = df.pivot_table(
    index='study_status',
    values='nct_number',
    aggfunc='count'
).sort_values('nct_number', ascending=False)

print("\n=== Pivot Table View ===")
print(pivot_table)

# === 4. Visualization ===
pivot_table.plot(kind='bar', legend=False, figsize=(10, 6))
plt.title('Clinical Trial Distribution by Study Status')
plt.xlabel('Study Status')
plt.ylabel('Number of Trials')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
