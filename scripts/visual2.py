import pandas as pd
import matplotlib.pyplot as plt
import os

# === 1. Load dataset ===
file_path = r'C:\Users\USER\Documents\DATA ANALYST\PROJECTS\Resume Projects\Project 2 Clinical Success & Dropout Analysis\clean_data\clinical_trials_clean_data.xlsx'
df = pd.read_excel(file_path)

# === 2. Ensure study_status and completion_date are clean ===
df['study_status'] = df['study_status'].fillna('Other')
df['completion_date'] = pd.to_datetime(df['completion_date'], errors='coerce')  # convert to datetime

# Filter only valid completion dates
df_valid = df.dropna(subset=['completion_date'])

# Extract year
df_valid['completion_year'] = df_valid['completion_date'].dt.year

# === 3. Calculate completion % per year ===
completion_summary = df_valid.groupby('completion_year')['study_status'].value_counts().unstack(fill_value=0)

# Add Completion % column
completion_summary['Completion_Percent'] = (completion_summary.get('Completed', 0) /
                                            completion_summary.sum(axis=1)) * 100

print(completion_summary[['Completed', 'Completion_Percent']])

# === 4. Plot line chart ===
plt.figure(figsize=(10,5))
plt.plot(completion_summary.index, completion_summary['Completion_Percent'], marker='o', linestyle='-', color='green')
plt.title('Clinical Trial Completion % Per Year')
plt.xlabel('Year')
plt.ylabel('Completion %')
plt.ylim(0, 100)
plt.grid(True)
plt.tight_layout()
plt.show()

# === 5. KPI card (overall completion %) ===
total_completed = (df_valid['study_status'] == 'Completed').sum()
total_trials = df_valid.shape[0]
overall_completion_pct = (total_completed / total_trials) * 100

print(f"\nKPI - Overall Completion Rate: {overall_completion_pct:.2f}%")

# === 6. Optional: Save chart & KPI summary ===
save_dir = r'C:\Users\USER\Documents\DATA ANALYST\PROJECTS\Resume Projects\Project 2 Clinical Success & Dropout Analysis\analysis\completion_percent_per_year.png'
os.makedirs(save_dir, exist_ok=True)

chart_path = os.path.join(save_dir, 'completion_percent_per_year.png')
plt.savefig(chart_path, dpi=300)

kpi_df = pd.DataFrame({'Metric': ['Overall Completion %'], 'Value': [overall_completion_pct]})
kpi_path = os.path.join(save_dir, 'completion_kpi.xlsx')
kpi_df.to_excel(kpi_path, index=False)

print(f"\nChart and KPI saved:\n- Chart: {chart_path}\n- KPI: {kpi_path}")
