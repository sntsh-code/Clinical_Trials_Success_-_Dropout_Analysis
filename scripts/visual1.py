import pandas as pd
import matplotlib.pyplot as plt

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
        return "Phase1"
    elif "phase0" in p:
        return "Phase0"
    elif p in ["", "na", "n/a", "not applicable"]:
        return "N/A"
    else:
        return "Other"

df["PhaseNormalized"] = df["phases"].apply(normalize_phase)

# === 3. Count trials per phase ===
phase_counts = df["PhaseNormalized"].value_counts().sort_index()

print("Phase-wise trial counts:")
print(phase_counts)

# === 4. Save to ===


# === 4. Plot both bar and pie side by side ===
fig, ax = plt.subplots(1, 2, figsize=(12,12))

# Bar chart
ax[0].bar(phase_counts.index, phase_counts.values)
ax[0].set_title("Phase-wise Distribution (Bar Chart)")
ax[0].set_xlabel("Trial Phase")
ax[0].set_ylabel("Number of Trials")
ax[0].tick_params(axis='x', rotation=45)

# Pie chart
ax[1].pie(
    phase_counts,
    labels=phase_counts.index,
    autopct='%1.1f%%',
    startangle=90,
    textprops={'fontsize': 7}
)
ax[1].set_title("Phase-wise Distribution (Pie Chart)")

plt.tight_layout()
plt.show()
