import pandas as pd


# === Load dataset ===
file_path = r'C:\Users\USER\Documents\DATA ANALYST\PROJECTS\Resume Projects\Project 2 Clinical Success & Dropout Analysis\clean_data\clinical_trials_clean_data.xlsx'
df = pd.read_excel(file_path)

# === Determine study period range ===
df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
df['completion_date'] = pd.to_datetime(df['completion_date'], errors='coerce')

total_trials = len(df)
start_year = df['start_date'].dt.year.min()
end_year = df['completion_date'].dt.year.max()

print(f"A total of {total_trials} trials were examined, spanning from {start_year} to {end_year}.")
