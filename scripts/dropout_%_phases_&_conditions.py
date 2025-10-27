import pandas as pd
import os

# === Load dataset ===
file_path = r'C:\Users\USER\Documents\DATA ANALYST\PROJECTS\Resume Projects\Project 2 Clinical Success & Dropout Analysis\clean_data\clinical_trials_clean_data.xlsx'
df = pd.read_excel(file_path)

# === Standardize study_status text ===
df['study_status'] = df['study_status'].str.strip().str.lower()

# === 1. Define dropout and completion categories ===
dropout_statuses = ['terminated', 'withdrawn', 'suspended']
completed_statuses = ['completed']

# === 2. Flag trials as dropout or completed ===
df['is_dropout'] = df['study_status'].isin(dropout_statuses)
df['is_completed'] = df['study_status'].isin(completed_statuses)

# === 3. Dropout % by Phase ===
phase_summary = (
    df.groupby('phases')
      .agg(total_trials=('nct_number', 'count'),
           dropout_trials=('is_dropout', 'sum'),
           completed_trials=('is_completed', 'sum'))
      .reset_index()
)
phase_summary['dropout_percent'] = (phase_summary['dropout_trials'] / phase_summary['total_trials'] * 100).round(2)

# === 4. Dropout % by Condition ===
condition_summary = (
    df.groupby('conditions')
      .agg(total_trials=('nct_number', 'count'),
           dropout_trials=('is_dropout', 'sum'),
           completed_trials=('is_completed', 'sum'))
      .reset_index()
)
condition_summary['dropout_percent'] = (condition_summary['dropout_trials'] / condition_summary['total_trials'] * 100).round(2)

# === 5. Sort results for readability ===
phase_summary.sort_values('dropout_percent', ascending=False, inplace=True)
condition_summary.sort_values('dropout_percent', ascending=False, inplace=True)

# === 6. Display ===
print("\n=== Dropout % by Phase ===")
print(phase_summary)

print("\n=== Dropout % by Condition ===")
print(condition_summary.head(15))  # top 15 for readability

# === 7. Save results ===
output_path = r'C:\Users\USER\Documents\DATA ANALYST\PROJECTS\Resume Projects\Project 2 Clinical Success & Dropout Analysis\analysis\dropout_analysis.xlsx'

with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    phase_summary.to_excel(writer, index=False, sheet_name='By_Phase')
    condition_summary.to_excel(writer, index=False, sheet_name='By_Condition')

print("\nDropout analysis saved at:")
print(output_path)
