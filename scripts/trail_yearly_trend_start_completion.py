import pandas as pd
import matplotlib.pyplot as plt
import os

# === Load cleaned dataset ===
file_path = r'C:\Users\USER\Documents\DATA ANALYST\PROJECTS\Resume Projects\Project 2 Clinical Success & Dropout Analysis\clean_data\clinical_trials_clean_data.xlsx'
df = pd.read_excel(file_path)

# === Convert date columns to datetime ===
df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
df['completion_date'] = pd.to_datetime(df['completion_date'], errors='coerce')

# === Extract years ===
df['start_year'] = df['start_date'].dt.year
df['completion_year'] = df['completion_date'].dt.year

# === Group by year ===
start_trends = df.groupby('start_year')['nct_number'].count().reset_index(name='initiated_trials')
completion_trends = df.groupby('completion_year')['nct_number'].count().reset_index(name='completed_trials')

# === Merge both on year ===
yearly_trends = pd.merge(start_trends, completion_trends,
                         left_on='start_year', right_on='completion_year',
                         how='outer').fillna(0)

# === Clean up column names ===
yearly_trends['year'] = yearly_trends['start_year'].combine_first(yearly_trends['completion_year']).astype(int)
yearly_trends = yearly_trends[['year', 'initiated_trials', 'completed_trials']].sort_values('year')

print("\n=== Yearly Trends in Trial Initiation and Completion ===")
print(yearly_trends.tail(15))  # recent years

# === Visualization ===
plt.figure(figsize=(10, 6))
plt.plot(yearly_trends['year'], yearly_trends['initiated_trials'], marker='o', label='Initiated Trials')
plt.plot(yearly_trends['year'], yearly_trends['completed_trials'], marker='s', label='Completed Trials')
plt.title('Yearly Trends in Clinical Trial Initiation and Completion')
plt.xlabel('Year')
plt.ylabel('Number of Trials')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# === Save summary ===
output_path = r'C:\Users\USER\Documents\DATA ANALYST\PROJECTS\Resume Projects\Project 2 Clinical Success & Dropout Analysis\analysis\yearly_trends_initiation_completion.xlsx'

with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    yearly_trends.to_excel(writer, index=False, sheet_name='Yearly_Trends')

print("\nYearly trend analysis saved at:")
print(output_path)
