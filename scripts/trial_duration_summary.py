import pandas as pd
import matplotlib.pyplot as plt
import os

# === 1. Load dataset ===
file_path = r'C:\Users\USER\Documents\DATA ANALYST\PROJECTS\Resume Projects\Project 2 Clinical Success & Dropout Analysis\raw_data\clinical_trials_raw_data.xlsx'
df = pd.read_excel(file_path)

# === 2. Normalize the "phases" column ===
def normalize_phase(phase):
    if pd.isna(phase):
        return "N/A"
    p = str(phase).strip().lower()
    if "phase4" in p or "phase iv" in p:
        return "Phase4"
    elif "phase3" in p or "phase iii" in p:
        return "Phase3"
    elif "phase2" in p or "phase ii" in p:
        return "Phase2"
    elif "phase1" in p or "phase i" in p or "early phase 1" in p:
        return "Phase 1"
    elif "phase0" in p:
        return "Phase0"
    elif p in ["", "na", "n/a", "not applicable"]:
        return "N/A"
    else:
        return "Other"

df["PhaseNormalized"] = df["phases"].apply(normalize_phase)

# === 3. Count trials per phase ===
phase_counts = df["PhaseNormalized"].value_counts().sort_index()

# === 4. Plot charts ===
fig, ax = plt.subplots(1, 2, figsize=(12, 12))

# Bar
ax[0].bar(phase_counts.index, phase_counts.values, color='steelblue')
ax[0].set_title("Phase-wise Distribution (Bar Chart)")
ax[0].set_xlabel("Trial Phase")
ax[0].set_ylabel("Number of Trials")
ax[0].tick_params(axis='x', rotation=45)

# Pie
ax[1].pie(
    phase_counts,
    labels=phase_counts.index,
    autopct='%1.1f%%',
    startangle=90,
    textprops={'fontsize': 9}
)
ax[1].set_title("Phase-wise Distribution (Pie Chart)")

plt.tight_layout()

# === 5. Create output folder ===
save_dir = r'C:\Users\USER\Documents\DATA ANALYST\PROJECTS\Resume Projects\Project 2 Clinical Success & Dropout Analysis\analysis\clinical_trail_phases_normalized.xlsx'
os.makedirs(save_dir, exist_ok=True)

# === 6. Save the chart ===
chart_path = os.path.join(save_dir, 'phase_wise_distribution.png')
plt.savefig(chart_path, dpi=300)
plt.show()

# === 7. Save the cleaned data ===
excel_path = os.path.join(save_dir, 'clinical_trials_phase_normalized.xlsx')
df.to_excel(excel_path, index=False)

print(f"Files saved:\n- Cleaned data: {excel_path}\n- Chart image:  {chart_path}")

# === Your summary data ===
data = {
    'Phase': ['Other', 'Phase 1', 'Phase 2', 'Phase 3', 'Phase 4'],
    'Trial_Count': [11, 130, 361, 47, 2]
}

df = pd.DataFrame(data)

# === Create output folder ===
save_dir = r'C:\Users\USER\Documents\DATA ANALYST\PROJECTS\Resume Projects\Project 2 Clinical Success & Dropout Analysis\analysis\phase_wise_distribution_summary.xlsx'
os.makedirs(save_dir, exist_ok=True)

# === Define save paths ===
excel_path = os.path.join(save_dir, 'phase_wise_distribution_summary.xlsx')
csv_path = os.path.join(save_dir, 'phase_wise_distribution_summary.csv')

# === Save to both Excel and CSV ===
df.to_excel(excel_path, index=False)
df.to_csv(csv_path, index=False)

print(f"Summary saved successfully:\n- Excel: {excel_path}\n- CSV:   {csv_path}")
