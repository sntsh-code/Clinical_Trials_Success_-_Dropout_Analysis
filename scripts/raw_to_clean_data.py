import pandas as pd
import os

# === Load dataset ===
file_path = r'C:\Users\USER\Documents\DATA ANALYST\PROJECTS\Resume Projects\Project 2 Clinical Success & Dropout Analysis\raw_data\clinical_trials_raw_data.xlsx'

if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found at: {file_path}")

df = pd.read_excel(file_path)

# === 1. Basic structure check ===
print("Original shape:", df.shape)
print("Columns:", list(df.columns))

# === 2. Drop duplicates ===
df.drop_duplicates(inplace=True)

# === 3. Handle missing values ===
# Drop rows with no core identifiers or study info
df.dropna(subset=['nct_number', 'study_title'], inplace=True)

# Fill selective columns with default values
fill_defaults = {
    'study_status': 'Unknown',
    'study_results': 'Not Reported',
    'conditions': 'Not Specified',
    'interventions': 'Not Specified',
    'primary_outcome_measures': 'Not Mentioned',
    'sponsor': 'Unknown Sponsor',
    'collaborators': 'None',
    'sex': 'All',
    'age': 'All',
    'phases': 'Not Applicable',
    'funder_type': 'Unknown',
    'study_type': 'Unspecified',
    'locations': 'Not Provided'
}
df.fillna(value = fill_defaults, inplace = True)

# === 4. Clean text data ===
text_cols = [
    'study_title', 'study_status', 'study_results', 'conditions', 'interventions',
    'primary_outcome_measures', 'sponsor', 'collaborators', 'sex', 'age',
    'phases', 'funder_type', 'study_type', 'locations'
]

for col in text_cols:
    df[col] = df[col].astype(str).str.strip().str.replace(r'\s+', ' ', regex=True).str.title()

# === 5. Clean numeric columns ===
# Convert enrollment_count to integer, handle bad values
df['enrollment_count'] = pd.to_numeric(df['enrollment_count'], errors='coerce')
df = df[df['enrollment_count'].notna()]  # remove rows where enrollment isn't numeric
df = df[df['enrollment_count'] > 0]       # keep only positive enrollments

# === 6. Standardize categorical fields ===
df['sex'] = df['sex'].replace({
    'M': 'Male', 'F': 'Female', 'Both': 'All', 'Na': 'All'
})
df['study_status'] = df['study_status'].replace({
    'Completed ': 'Completed', 'Terminated ': 'Terminated'
})

# === 7. Parse dates ===
df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
df['completion_date'] = pd.to_datetime(df['completion_date'], errors='coerce')

# === 8. Remove logically inconsistent rows ===
# Drop if completion_date < start_date (invalid timelines)
df = df[(df['completion_date'].isna()) | (df['start_date'].isna()) | (df['completion_date'] >= df['start_date'])]

# === 9. Final sanity check ===
print("Cleaned shape:", df.shape)

# === 10. Save cleaned data ===
clean_path = r'C:\Users\USER\Documents\DATA ANALYST\PROJECTS\Resume Projects\Project 2 Clinical Success & Dropout Analysis\clean_data\clinical_trials_clean_data.xlsx'
os.makedirs(os.path.dirname(clean_path), exist_ok=True)
df.to_excel(clean_path, index=False)

print("Data cleaning complete! Clean file saved to:")
print(clean_path)