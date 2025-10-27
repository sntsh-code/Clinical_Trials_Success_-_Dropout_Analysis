import pandas as pd
import matplotlib.pyplot as plt
import os

# === Load cleaned data ===
file_path = r'C:\Users\USER\Documents\DATA ANALYST\PROJECTS\Resume Projects\Project 2 Clinical Success & Dropout Analysis\clean_data\clinical_trials_clean_data.xlsx'
df = pd.read_excel(file_path)

# === Normalize study_status text ===
df['study_status'] = df['study_status'].str.strip().str.lower()

# === Define completion/dropout categories ===
dropout_statuses = ['terminated', 'withdrawn', 'suspended']
completed_statuses = ['completed']

# === Flag records ===
df['is_dropout'] = df['study_status'].isin(dropout_statuses)
df['is_completed'] = df['study_status'].isin(completed_statuses)

# === Aggregate by sponsor ===
sponsor_summary = (
    df.groupby('sponsor')
      .agg(total_trials=('nct_number', 'count'),
           dropout_trials=('is_dropout', 'sum'),
           completed_trials=('is_completed', 'sum'))
      .reset_index()
)

# === Calculate percentages ===
sponsor_summary['dropout_percent'] = (sponsor_summary['dropout_trials'] / sponsor_summary['total_trials'] * 100).round(2)
sponsor_summary['completion_percent'] = (sponsor_summary['completed_trials'] / sponsor_summary['total_trials'] * 100).round(2)

# === Get Top 15 sponsors by total trial volume ===
top_sponsors = sponsor_summary.sort_values('total_trials', ascending=False).head(15)

print("\n=== Top 15 Sponsors: Dropout & Completion Rates ===")
print(top_sponsors[['sponsor', 'total_trials', 'dropout_percent', 'completion_percent']])

# === Visualization ===
plt.figure(figsize=(10, 6))
plt.barh(top_sponsors['sponsor'], top_sponsors['completion_percent'], label='Completion %')
plt.barh(top_sponsors['sponsor'], top_sponsors['dropout_percent'], left=top_sponsors['completion_percent'], label='Dropout %')
plt.xlabel('Percentage')
plt.ylabel('Sponsor')
plt.title('Top 15 Sponsors: Dropout vs Completion Rates')
plt.legend()
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# === Save summary ===
output_path = r'C:\Users\USER\Documents\DATA ANALYST\PROJECTS\Resume Projects\Project 2 Clinical Success & Dropout Analysis\analysis\sponsor_dropout_completion.xlsx'

with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    sponsor_summary.to_excel(writer, index=False, sheet_name='Sponsor_Stats')
    top_sponsors.to_excel(writer, index=False, sheet_name='Top15_Sponsors')

print("\nSponsor dropout & completion summary saved at:")
print(output_path)
